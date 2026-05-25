from typing import Any


def choicer(
    opciones: list[Any], mensaje: str = "Elegí una opción"
) -> (
    int
):  # le da al usuario un menú de opciones para elegir, devuelve el índice de la opción elegida
    lngth = len(opciones)
    if lngth < 2:
        raise ValueError("Deben haber por lo menos dos opciones.")

    mensaje += f" [1-{lngth}]: "
    while True:
        for i, opcion in enumerate(opciones):
            print(f"{i+1}. {opcion}")
        try:
            eleccion = int(input(mensaje))
            if 1 <= eleccion <= lngth:
                return eleccion - 1
            else:
                print(f"Por favor, ingresá un número entre 1 y {lngth}.")
        except ValueError:
            print("Entrada no válida. Por favor, ingresá un número.")

def caso_imposible(choice: int, opciones:list[Any]):
    raise IndexError(f"Error en choicer: Devolvió un índice imposible {choice} para una lista de {len(opciones)} elementos")