from pathlib import Path
from . import csv_io
from .custom_types import a_clima, Clima, a_clima_csv
from datetime import datetime

path_csv_historial = Path("csv/historial_global.csv")
COLUMNAS_CSV_HISTORIAL = [
    "NombreDeUsuario",
    "Ciudad",
    "FechaHoraCompleta",
    "Temperatura_C",
    "Sensacion_Termica",
    "Condicion_Clima",
    "Humedad_Porcentaje",
    "Viento_kmh",
]
historial_global: list[Clima] = [
    a_clima(
        {
            "NombreDeUsuario": c["NombreDeUsuario"],
            "Ciudad": c["Ciudad"],
            "FechaHoraCompleta": c[
                "FechaHoraCompleta"
            ],  # a_clima la convierte sola a datetime
            "Temperatura_C": float(c["Temperatura_C"]),
            "Sensacion_Termica": float(c["Sensacion_Termica"]),
            "Condicion_Clima": c["Condicion_Clima"],
            "Humedad_Porcentaje": float(c["Humedad_Porcentaje"]),
            "Viento_kmh": float(c["Viento_kmh"]),
        }
    )
    for c in csv_io.leer_o_crear(path_csv_historial, COLUMNAS_CSV_HISTORIAL)
]


def dump():
    csv_io.escribir(
        path_csv_historial,
        COLUMNAS_CSV_HISTORIAL,
        [a_clima_csv(c) for c in historial_global],
    )


def agregar_datos(d: Clima):
    historial_global.append(d)
    dump()


# Devuelve una lista con los nombres completos ("Buenos Aires, AR") de todas las
# ciudades que recibieron consultas en orden alfabético.
def todas_las_ciudades():
    ciudades = list(set(c["Ciudad"] for c in historial_global))
    return sorted(ciudades)


def ciudades_del_usuario(username: str) -> list[str]:
    ciudades = list(
        {c["Ciudad"] for c in historial_global if c["NombreDeUsuario"] == username}
    )
    return sorted(ciudades)


def ciudad_mas_consultada() -> str | None:
    conteo_por_ciudad: dict[str, int] = {}
    for consulta in historial_global:
        ciudad = consulta["Ciudad"]
        conteo_por_ciudad[ciudad] = conteo_por_ciudad.get(ciudad, 0) + 1

    ciudad_mas_consultada, _ = max(conteo_por_ciudad.items(), key=lambda item: item[1])
    return ciudad_mas_consultada


def total_consultas() -> int:
    return len(historial_global)


def temperatura_promedio() -> float | None:
    if not historial_global:
        return None

    total_temp = sum(c["Temperatura_C"] for c in historial_global)
    return total_temp / len(historial_global)


# Ej. Pasando (usr1, "Buenos Aires, AR"), devuelve todas las veces en las que
# el usr1 consultó el clima de Buenos Aires como lista de Climas, ordenadas por
# fecha (de más reciente a más antigua)
def obtener_historial_personal_ciudad(username: str, ciudad: str) -> list[Clima]:
    return sorted(
        [
            c
            for c in historial_global
            if c["NombreDeUsuario"] == username and c["Ciudad"] == ciudad
        ],
        key=lambda c: c["FechaHoraCompleta"],
        reverse=True,
    )


def obtener_ultima_consulta(username: str) -> Clima | None:
    """Devuelve el registro más reciente para el usuario, o None si no tiene consultas."""
    consultas_usuario = [
        c for c in historial_global if c["NombreDeUsuario"] == username
    ]
    if not consultas_usuario:
        return None

    return max(consultas_usuario, key=lambda c: c["FechaHoraCompleta"])


def exportar_historial():
    now = datetime.now()
    timestamp = now.strftime("%Y%m%d%H%M%S")
    path = Path(f"csv/out/historial_global_{timestamp}.csv")
    csv_io.escribir(
        path,
        COLUMNAS_CSV_HISTORIAL,
        [a_clima_csv(c) for c in historial_global],
    )
    print(f"Historial global exportado a {path}")
