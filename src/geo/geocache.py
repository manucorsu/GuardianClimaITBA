from ..custom_types import Ciudad, a_ciudad
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
    # Verifica si la ciudad ya existe usando su nombre completo, lo cual significa que bajo ciertas circunstancias puede hacer que dos ciudades
    # lejanas en el mismo país (ej. Portland, Oregon y Portland, Maine en Estados Unidos) puedan quedar agrupadas como la misma ciudad. Sin
    # embargo, como la información de las provincias/estados en las que están las distintas ciudades no siempre aparece y cuando lo hace
    # está únicamente en inglés (quedaría raro ver "Buenos Aires, Autonomous City of Buenos Aires, AR" en una aplicación en español) y la
    # consigna ni siquiera solicita el país, asumimos que esta limitación no tendría gram importancia.
    existing_idx = None
    for i, c in enumerate(_cache):
        if ciudad_nueva["nombre_completo"] == c["nombre_completo"]:
            existing_idx = i
            c["otros_nombres"] = list(
                set(c["otros_nombres"] + ciudad_nueva["otros_nombres"])
            )  # list(set()) elimina duplicados
            _cache[i] = c
            break
    if existing_idx is None:
        _cache.append(ciudad_nueva)

    dump()

    if existing_idx is None:
        return ciudad_nueva
    else:
        return _cache[existing_idx]
