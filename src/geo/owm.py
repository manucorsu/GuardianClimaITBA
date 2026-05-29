from typing import Any
import requests
from ..types import Ciudad
from ..secrets import owm_api_key
from . import geocache
from json import JSONDecodeError

assert owm_api_key is not None  # main no permite que este módulo llegue a abrirse
# si no está la API key (cierra todo en el momento), esto es solo para satisfacer
# al typechecker

# Aclaración importante: Si bien la consigna mostraba la base URL de la versión
# 2.5 que sigue funcionando y no requiere hacer el geocoding por separado, también
# decía que esta URL era "aproximada" y sugería fuertemente revisar la documentación.
# La misma (https://openweathermap.org/api/one-call-4), no muestra a ninguna versión
# inferior a la 3.0, lo que da a entender que la versión 2.5 fue discontinuada;
# Investigando un poco más, esta versión dejó de ser soportada hace casi dos años en
# junio de 2024 (https://openweathermap.org/api/one-call-transfer), por lo que
# decidimos seguir lo que recomienda la documentación actual y usar la versión estable
# más nueva, la 4.0, incluso si eso implicaba tener que realizar algún paso de más.

BASE_URL_CLIMA = "https://api.openweathermap.org/data/4.0/onecall/current"
UNITS_CLIMA = "metric"
LANG_CLIMA = "es"

TIMEOUT = 25

BASE_URL_GEOCODING = "https://api.openweathermap.org/geo/1.0/direct"
LIMIT_GEOCODING = 1


def handle_owm_errors(
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


def geocode_nombre_ciudad(ciudad: str) -> Ciudad | None:
    # En cumplimiento con el handling propuesto en la consigna (que es para la versión 2.5 que no requiere este paso),
    # devuelve None si no se encuentra ninguna ciudad o encuentra un error, print()eando adecuadamente
    print("Buscando la ciudad", end="")
    c_en_cache = geocache.ciudad_en_cache(ciudad)
    if c_en_cache:
        print("...✅ Encontrada en caché.")
        return c_en_cache
    print(" por geocoding...", end="")
    parametros: dict[str, Any] = {
        "q": ciudad,
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
        return handle_owm_errors(ex, respuesta, ciudad)
    nom = None
    try:
        english_name = datos_ciudad["name"]  # Toda respuesta válida lo tiene
        local_names = datos_ciudad.get("local_names")
        nombre_es = None
        if local_names:
            nombre_es = local_names.get("es")

        if not local_names or not nombre_es:
            nom = english_name
        else:
            nom = nombre_es
        assert isinstance(nom, str)
        # Primero intenta buscar el nombre en español, si no está agarra el
        # "name" genérico en inglés que siempre está presente.
        # Todos los asserts en esta función (y en general en todo el proyecto) nunca
        # resultarán en AssertionError y están solo para que se conserven los tipos
        # como una ayuda de escritura para nosotros.
        pais = datos_ciudad["country"]
        assert isinstance(pais, str)
        nombre_completo = f"{nom}, {pais}"

        lat = datos_ciudad["lat"]
        assert isinstance(lat, (int, float))

        lon = datos_ciudad["lon"]
        assert isinstance(lon, (int, float))

        nu = ciudad.upper()
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
