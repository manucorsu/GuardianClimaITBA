from pathlib import Path
from . import csv_io
from .custom_types import a_clima, Clima, a_clima_csv

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


def historial_personal(username: str):
    return [c for c in historial_global if c["NombreDeUsuario"] == username]
