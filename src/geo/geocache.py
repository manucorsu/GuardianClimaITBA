from ..types import Ciudad, a_ciudad
from pathlib import Path
import json

_path = Path("geocache/geocache.json")

_cache: list[Ciudad] = []

try:
    with open(_path, "r") as f:
        data = json.load(f)
        for el in list(data):
            _cache.append(a_ciudad(dict(el)))

except FileNotFoundError:
    pass
    # después cuando se agregue la primera ciudad se `dump()`ea
    # automáticamente


def ciudad_en_cache(nombre: str):
    for c in _cache:
        if nombre.upper() in c["otros_nombres"] + [c["nombre_completo"].upper()]:
            return c
    return None


def dump():
    _path.parent.mkdir(parents=True, exist_ok=True)
    with open(_path, "w") as f:
        json.dump(_cache, f)


def agregar_ciudad_nueva(ciudad_nueva: Ciudad) -> Ciudad:
    # Agrega una ciudad nueva al cache.
    # Primero verifica si es realmente una ciudad nueva y no solo un nombre alternativo para una ya existente. En caso de que ya exista, devuelve el
    # dict de ciudad existente con el nombre nuevo agregado; Si es verdaderamente una ciudad nueva solo devuelve el mismo diccionario que se pasó.
    # En cualquier caso agrega la ciudad nueva/actualiza la existente en el caché y lo dumpea.
    existing_idx = None
    for i, c in enumerate(_cache):
        if ciudad_nueva["nombre_completo"] == c["nombre_completo"] and (
            int(ciudad_nueva["lat"]),
            int(ciudad_nueva["lon"]),
        ) == (int(c["lat"]), int(c["lon"])):
            # Como en el mundo existen ciudades lejanas con el mismo nombre (ej. Arlington, Texas y Arlington, Virginia), se
            # considera la ciudad ya existe si tiene el mismo nombre y están "más o menos" en el mismo lugar truncando las coordenadas a int.
            existing_idx = i
            c["otros_nombres"] = list(
                set(c["otros_nombres"] + ciudad_nueva["otros_nombres"])
            )  # list(set()) elimina duplicados
            _cache[i] = c
            break
    if not existing_idx:
        _cache.append(ciudad_nueva)

    dump()

    if not existing_idx:
        return ciudad_nueva
    else:
        return _cache[existing_idx]
