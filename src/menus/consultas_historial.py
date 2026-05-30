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


def estadisticas_globales():
    clear()
    print("--Estadísticas globales de uso--")
    ciudad = historial.ciudad_mas_consultada()
    total = historial.total_consultas()
    temp_promedio = historial.temperatura_promedio()

    if total == 0:
        print("No hay consultas registradas en el historial global.")
    else:
        print(f"Ciudad más consultada: {ciudad}")
        print(f"Total de consultas: {total}")
        print(f"Temperatura promedio registrada: {temp_promedio:.2f} °C")

    historial.exportar_historial()
    input("\nPresiona Enter para volver al menú principal...")
