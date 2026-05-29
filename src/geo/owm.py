from typing import Any
import requests
from numbers import Number
from ..types import Ciudad
from ..secrets import owm_api_key
from . import geocache

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
# más nueva, la 4.0 incluso si eso implicaba tener que realizar algún paso de más.

BASE_URL_CLIMA = "https://api.openweathermap.org/data/4.0/onecall/current"
UNITS_CLIMA = "metric"
LANG_CLIMA = "es"

TIMEOUT = 25

BASE_URL_GEOCODING = "https://api.openweathermap.org/geo/1.0/direct"
LIMIT_GEOCODING = 1


def geocode_nombre_ciudad(ciudad: str) -> Ciudad:
    # TODO: handling a la javier apat
    print("Buscando la ciudad...")
    c_en_cache = geocache.ciudad_en_cache(ciudad)
    if c_en_cache:
        print("La ciudad estaba cacheada, devolviendo lat/lon...")
        return c_en_cache
    print("Buscando la ciudad por geocoding...")
    parametros: dict[str, Any] = {
        "q": ciudad,
        "appid": owm_api_key,
        "limit": LIMIT_GEOCODING,
    }

    respuesta = requests.get(BASE_URL_GEOCODING, params=parametros, timeout=TIMEOUT)
    respuesta.raise_for_status()
    datos_ciudad = None
    try:
        datos_ciudad = (respuesta.json())[0]
    except (
        KeyError
    ):  # Cuando no encuentra nada devuelve un array vacío con status 200, no 404
        raise ValueError(
            f"No se encontró una ciudad de nombre '{ciudad}', revisá que esté bien escrito."
        )

    nom = None
    try:
        nom = datos_ciudad["local_names"]["es"]
    except KeyError:
        nom = datos_ciudad["name"]
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
    assert isinstance(lat, Number)

    lon = datos_ciudad["lon"]
    assert isinstance(lon, Number)

    nu = ciudad.upper()
    nueva_c: Ciudad = {
        "nombre_completo": nombre_completo,
        "lat": lat,
        "lon": lon,
        "otros_nombres": [nu] if nu != nombre_completo.upper() else [],
    }
    geocache.agregar_ciudad_nueva(nueva_c)
    return nueva_c
