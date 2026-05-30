from .. import historial
from ..choicer import choicer
from ..clear import clear


def historial_personal(username: str):
    print("--Consultar historial personal de consultas por ciudad--")
    print("¿De qué ciudad deseas conocer tu historial de consultas?")
    todas_las_ciudades = historial.todas_las_ciudades()
    ciudad = choicer(todas_las_ciudades)
    hpc = historial.obtener_historial_personal_ciudad(username, ciudad)
    clear()

    print(f"--Historial de consultas de {username} para {ciudad}--")
