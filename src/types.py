# acá van todos los tipos "custom" reutilizados a lo largo del proyecto
from enum import Enum
from typing import TypedDict, Any


class OpcionesMenu(Enum):
    def __str__(self) -> str:
        return self.value


# así, si todos los menúes heredan de esta para sus opciones,
# cuando choicer mostrará las opciones como sus valores y
# no `EnumName.MEMBER_NAME`


class Ciudad(TypedDict):
    nombre_completo: str  # ej. "Buenos Aires, AR"
    lat: int | float
    lon: int | float
    otros_nombres: list[str]


def a_ciudad(d: dict[Any, Any]) -> Ciudad:
    # se usa solo en geocache y no en la que obtiene el dato de
    # la API porque esa tiene un handling bastante diferente.
    nombre_completo = d["nombre_completo"]
    assert isinstance(nombre_completo, str)

    lat = d["lat"]
    assert isinstance(lat, (int, float))

    lon = d["lon"]
    assert isinstance(lat, (int, float))

    otros_nombres = list(d["otros_nombres"])
    for n in otros_nombres:
        assert isinstance(n, str)
        assert n.isupper()
    otros_nombres: list[str]

    c: Ciudad = {
        "nombre_completo": nombre_completo,
        "lat": lat,
        "lon": lon,
        "otros_nombres": otros_nombres,
    }
    return c
