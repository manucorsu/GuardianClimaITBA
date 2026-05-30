from tabulate import tabulate
from .. import historial
from ..choicer import choicer
from ..clear import clear
from typing import Any


def historial_personal(username: str):
    print("--Consultar historial personal de consultas por ciudad--")
    print("¿De qué ciudad deseas conocer tu historial de consultas?")
    todas_las_ciudades = historial.todas_las_ciudades()
    ciudad = choicer(todas_las_ciudades)
    hpc = historial.obtener_historial_personal_ciudad(username, ciudad)
    clear()

    print(f"--Historial de consultas de {username} para {ciudad}--")
    headers = [
        "Fecha y hora",
        "Temperatura (°C)",
        "Sensación térmica (°C)",
        "Condición del clima",
        "Humedad (%)",
        "Viento (km/h)",
    ]
    filas: list[list[Any]] = [
        [
            c["FechaHoraCompleta"],
            c["Temperatura_C"],
            c["Sensacion_Termica"],
            c["Condicion_Clima"],
            c["Humedad_Porcentaje"],
            c["Viento_kmh"],
        ]
        for c in hpc
    ]
    if not filas:
        print("No hay consultas para esta ciudad.")
        return

    print(tabulate(filas, headers=headers, tablefmt="grid", maxcolwidths=20))
