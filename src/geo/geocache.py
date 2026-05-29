from ..types import Ciudad
from pathlib import Path
import json

_path = Path("geocache/geocache.json")

_cache: list[Ciudad] = []

try:
    with open(_path, "r") as f:
        data = json.load(f)
        for el in list(data):
            assert isinstance(el, dict)

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


def agregar_ciudad_nueva(ciudad_nueva: Ciudad):
    realmente_nueva = True
    for i, c in enumerate(_cache):
        if (ciudad_nueva["lat"], ciudad_nueva["lon"]) == (c["lat"], c["lon"]):
            c["otros_nombres"] = list(
                set(c["otros_nombres"] + ciudad_nueva["otros_nombres"])
            )  # elimina duplicados
            _cache[i] = c
            realmente_nueva = False
            break
    if realmente_nueva:
        _cache.append(ciudad_nueva)

    dump()
