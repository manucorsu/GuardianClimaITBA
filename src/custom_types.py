# acá van todos los tipos "custom" reutilizados a lo largo del proyecto
from enum import Enum
from typing import TypedDict, Any, NotRequired
from datetime import datetime
from .geo.data_time import pretty_dt


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


# Representa datos de clima obtendidos de la API + el nombre de usuario
# del solicitante. Seguimos el formato de nombres de la página 3 de la consigna
class Clima(TypedDict):
    NombreDeUsuario: str  # Nombre del usuario
    Ciudad: str  # nombre_completo de una Ciudad

    FechaHoraCompleta: datetime

    Temperatura_C: int | float
    Sensacion_Termica: int | float
    Condicion_Clima: str
    Humedad_Porcentaje: int | float
    Viento_kmh: int | float

    icon_code: NotRequired[int]


def a_clima(o: Any) -> Clima:
    NombreDeUsuario = o["NombreDeUsuario"]
    assert isinstance(NombreDeUsuario, str)

    Ciudad = o["Ciudad"]
    assert isinstance(Ciudad, str)

    FechaHoraCompleta = o["FechaHoraCompleta"]
    assert isinstance(
        FechaHoraCompleta, (datetime, str)
    ), "FechaHoraCompleta debe ser un datetime o un isostring"
    if isinstance(FechaHoraCompleta, str):
        FechaHoraCompleta = datetime.fromisoformat(FechaHoraCompleta)
    Temperatura_C = o["Temperatura_C"]
    assert isinstance(
        Temperatura_C, (int, float)
    ), "La temperatura (en °C) debe ser un número"

    Sensacion_Termica = o["Sensacion_Termica"]
    assert isinstance(
        Sensacion_Termica, (int, float)
    ), "La sensación térmica (en °C) debe ser un número"

    Condicion_Clima = o["Condicion_Clima"]
    assert isinstance(
        Condicion_Clima, str
    ), "La descipción de la condición del clima debe ser un string."

    Humedad_Porcentaje = o["Humedad_Porcentaje"]
    assert isinstance(
        Humedad_Porcentaje, (int, float)
    ), "Humedad_Porcentaje debe ser un número"
    assert (
        0 <= Humedad_Porcentaje <= 100
    ), "El valor de Humedad_Porcentaje debe ser un porcentaje [0; 100]"

    Viento_kmh = o["Viento_kmh"]
    assert isinstance(
        Viento_kmh, (int, float)
    ), "La velocidad del viento tiene que ser un número >= 0"
    assert Viento_kmh >= 0, "La velocidad del viento tiene que ser un número >= 0"
    resultado: Clima = {
        "NombreDeUsuario": NombreDeUsuario,
        "Ciudad": Ciudad,
        "FechaHoraCompleta": FechaHoraCompleta,
        "Temperatura_C": Temperatura_C,
        "Sensacion_Termica": Sensacion_Termica,
        "Condicion_Clima": Condicion_Clima,
        "Humedad_Porcentaje": Humedad_Porcentaje,
        "Viento_kmh": Viento_kmh,
    }

    icon_code = o.get("icon_code")
    if icon_code:
        assert isinstance(
            icon_code, int
        ), "De incluirse, el icon_code debería ser un entero"
        assert icon_code in range(
            200, 900
        ), "de incluirse, icon_code debe ser ∈ [200;899]"
        # ver https://openweathermap.org/api/weather-conditions#Weather-Condition-Codes-2
        resultado["icon_code"] = icon_code
    return resultado


# No le hace ninguna modificación, solo cambia el tipo de FechaHoraCompleta a un
# str (su ISO datestring) para que sea representable en CSV, remueve el icon_code
# porque es innecesario y deja el tipo menos específico dict[str, int|float|str]
# en vez de un TypedDict para evitar problemas de chequeo con csv_io.escribir()
def a_clima_csv(c: Clima) -> dict[str, int | float | str]:
    return {
        "NombreDeUsuario": c["NombreDeUsuario"],
        "Ciudad": c["Ciudad"],
        "FechaHoraCompleta": c["FechaHoraCompleta"].isoformat(),
        "Temperatura_C": c["Temperatura_C"],
        "Sensacion_Termica": c["Sensacion_Termica"],
        "Condicion_Clima": c["Condicion_Clima"],
        "Humedad_Porcentaje": c["Humedad_Porcentaje"],
        "Viento_kmh": c["Viento_kmh"],
    }


# Versión simplificada y con emojis en vez de imágenes de
# https://openweathermap.org/api/weather-conditions
def emoji_descripcion(icon_code: int | None):
    if icon_code in range(200, 300):
        return "⛈️"
    elif icon_code in range(500, 505):
        return "🌦️"
    elif icon_code == 511 or icon_code in range(600, 700):
        return "❄️"
    elif icon_code in range(300, 400) or icon_code in range(520, 532):
        # no distinguimos entre lluvia y llovizna por falta de emojis
        return "🌧️"
    elif icon_code in range(700, 800):
        return "🌁"
    elif icon_code == 801:
        return "🌥️"
    elif icon_code in range(802, 900):
        return "☁️"
    else:
        return "☀️"


def pretty_print_informe(c: Clima):
    print(f"\n--Informe meteorológico de {c["Ciudad"]}--")
    print(f"🕒️ {pretty_dt(c["FechaHoraCompleta"])}")
    ed = emoji_descripcion(c.get("icon_code"))
    print(f"{ed}  {c["Condicion_Clima"]} {ed}")
    print(
        f"🌡️ Hacen {c["Temperatura_C"]}°C, con una sensación térmica de {c['Sensacion_Termica']}°C."
    )
    print(f"💧 El porcentaje de humedad es {c["Humedad_Porcentaje"]}%.")
    print(f"🍃 La velocidad del viento es de {c["Viento_kmh"]:.2f} km/h.\n")
