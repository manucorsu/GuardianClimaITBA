from typing import Any
import requests
from ..custom_types import Ciudad, Clima, a_clima
from ..secrets import owm_api_key
from . import geocache
from json import JSONDecodeError
from .data_time import api_dt_to_datetime
from .. import historial

assert owm_api_key is not None  # main no permite que este módulo llegue a abrirse
# si no está la API key (cierra todo en el momento), esto es solo para satisfacer
# al typechecker

# Aclaración importante: Si bien en la consigna no aparece como obligatorio hacer
# el geocoding por separado llamando a la otra API, en la documentación actual de
# OWM dice que el geocoding del endpoint /weather ha quedado obsoleto y solicitan
# utilizar la API de geocoding para obtener la latitud y longitud de la ciudad
# para solicitar a /weather con esos datos en vez del nombre. Como la consigna decía
# que la URL era "aproximada" y exigía revisar la documentación, decidimos seguir
# la recomendación oficial de la misma.

BASE_URL_CLIMA = "https://api.openweathermap.org/data/2.5/weather"
UNITS_CLIMA = "metric"
LANG_CLIMA = "es"

TIMEOUT = 30

BASE_URL_GEOCODING = "https://api.openweathermap.org/geo/1.0/direct"
LIMIT_GEOCODING = 1


def handle_owm_response_errors(
    ex: (
        IndexError
        | requests.exceptions.HTTPError
        | requests.exceptions.RequestException
        | JSONDecodeError
    ),
    res: requests.Response | None,
    n_cit: str | None = None,
) -> None:
    # basado en página 8 de la consigna
    print("❌.")

    def _handle_404():
        print(
            f"Error OWM: Ciudad '{n_cit}' no encontrada. Verificá que esté bien escrito el nombre."
        )
        # podemos usar n_cit porque solo el geocoding puede
        # "tirar 404" (IndexError)

    if isinstance(ex, IndexError):
        return _handle_404()
    elif isinstance(ex, requests.exceptions.HTTPError):
        if res is None:
            print(f"Error HTTP OWM: {ex}")
            return
        match (res.status_code):
            case 401:
                print(
                    "Error de autenticación OWM: API Key inválida, es decir, el valor de OWM_API_KEY en .env es incorrecto. Si aún deseas usar las funciones de búsqueda de clima, tenés que cerrar la aplicación, colocar el valor correcto y volverla a abrir."
                )
                return
            case 404:
                return _handle_404()
            case _:
                print(f"Error HTTP OWM: {ex}")
                return
    elif isinstance(ex, requests.exceptions.RequestException):
        print(f"Error de conexión/petición OWM: {ex}")
        return
    else:  # (JSONDecodeError)
        print("Error OWM: La respuesta de la API no es JSON válido")
        return


def geocode_nombre_ciudad(nombre_ciudad: str) -> Ciudad | None:
    # En cumplimiento con el handling propuesto en la consigna (que es para la versión 2.5 que no requiere este paso),
    # devuelve None si no se encuentra ninguna ciudad o encuentra un error, print()eando adecuadamente
    print("Buscando la ciudad", end="")
    c_en_cache = geocache.ciudad_en_cache(nombre_ciudad)
    if c_en_cache:
        print("...✅ Encontrada en caché.")
        return c_en_cache
    print(" por geocoding...", end="")
    parametros: dict[str, Any] = {
        "q": nombre_ciudad,
        "appid": owm_api_key,
        "limit": LIMIT_GEOCODING,
    }

    datos_ciudad = None
    respuesta = None
    try:
        respuesta = requests.get(BASE_URL_GEOCODING, params=parametros, timeout=TIMEOUT)
        respuesta.raise_for_status()
        datos_ciudad = (respuesta.json())[0]
        # cuando no encuentra nada, no devuelve un error con 404 sino que
        # con el status 200 devuelve una lista vacía, de esta forma si
        # lo está levantamos un IndexError que handleamos como pide la
        # consigna que se handleen los 404

    except (
        IndexError,
        requests.exceptions.HTTPError,
        requests.exceptions.RequestException,
        JSONDecodeError,
    ) as ex:
        return handle_owm_response_errors(ex, respuesta, nombre_ciudad)
    nom = None
    try:
        english_name = datos_ciudad["name"]  # Toda respuesta válida lo tiene
        local_names = datos_ciudad.get("local_names")
        nombre_es = None
        if local_names:
            nombre_es = local_names.get(LANG_CLIMA)

        if not local_names or not nombre_es:
            nom = english_name
        else:
            nom = nombre_es
        assert isinstance(
            nom, str
        ), "OWM debería haber provisto un string para el nombre"
        # Primero intenta buscar el nombre en español, si no está agarra el
        # "name" genérico en inglés que siempre está presente.
        # Todos los asserts en esta función (y en general en todo el proyecto) nunca
        # resultarán en AssertionError y están solo para que se conserven los tipos
        # como una ayuda de escritura para nosotros.

        pais = datos_ciudad["country"]
        assert isinstance(
            pais, str
        ), "OWM debería haber provisto un string para el país"
        nombre_completo = f"{nom}, {pais}"

        lat = datos_ciudad["lat"]
        assert isinstance(
            lat, (int, float)
        ), "OWM debería haber provisto un número para la latitud"

        lon = datos_ciudad["lon"]
        assert isinstance(
            lon, (int, float)
        ), "OWM debería haber provisto un número para la longitud"

        nu = nombre_ciudad.upper()
        nueva_c: Ciudad = {
            "nombre_completo": nombre_completo,
            "lat": lat,
            "lon": lon,
            "otros_nombres": [nu] if nu != nombre_completo.upper() else [],
        }
        print("✅ Encontrada.")
        return geocache.agregar_ciudad_nueva(nueva_c)
    except (KeyError, AssertionError, TypeError, AttributeError) as ex:
        print(
            f"❌.\nError: formato inesperado de datos de OWM geocoding. Más info.: {ex}"
        )
        return


def _buscar_clima_raw(ciudad: Ciudad) -> Any | None:
    print(f"Buscando los datos del clima en {ciudad['nombre_completo']}...", end="")
    parametros: dict[str, Any] = {
        "lat": ciudad["lat"],
        "lon": ciudad["lon"],
        "appid": owm_api_key,
        "units": UNITS_CLIMA,
        "lang": LANG_CLIMA,
    }
    respuesta = None
    datos_clima = None
    try:
        respuesta = requests.get(BASE_URL_CLIMA, params=parametros, timeout=TIMEOUT)
        respuesta.raise_for_status()
        datos_clima = respuesta.json()
        print("✅.")
        return datos_clima
    except (
        requests.exceptions.HTTPError,
        requests.exceptions.RequestException,
        JSONDecodeError,
    ) as ex:
        return handle_owm_response_errors(ex, respuesta)


def buscar_clima(username: str, ciudad: Ciudad) -> Clima | None:
    datos_clima = _buscar_clima_raw(ciudad)
    if (
        datos_clima is None
    ):  # sigifica que ocurrió un error que ya fue mostrado (handleado)
        return datos_clima
    print("Procesando los datos...", end="")
    try:
        resultado = a_clima(
            {
                "NombreDeUsuario": username,
                "Ciudad": ciudad["nombre_completo"],
                "FechaHoraCompleta": api_dt_to_datetime(
                    datos_clima["dt"], datos_clima["timezone"]
                ),
                "Temperatura_C": datos_clima["main"]["temp"],
                "Sensacion_Termica": datos_clima["main"]["feels_like"],
                "Condicion_Clima": datos_clima["weather"][0]["description"],
                "Humedad_Porcentaje": datos_clima["main"]["humidity"],
                "Viento_kmh": datos_clima["wind"]["speed"]
                * 3.6,  # según la documentación viene en metros por segundo así que se convierte a kmh así
                "icon_code": datos_clima["weather"][0]["id"],
            }
        )
        print("✅.\nGuardando en historial...", end="")
        historial.agregar_datos(resultado)
        print("✅.")
        print("Mostrando los datos...")
        return resultado
    except (TypeError, AssertionError, ValueError, KeyError) as ex:
        print(f"❌. Error de la respuesta OWM: ({type(ex)}) {ex}")
        raise ex
