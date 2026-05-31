from .clear import clear
from typing import TypeVar

T = TypeVar("T")


# Hace que el usuario elija un elemento de la lista y devuelve ese elemento.
# Usa T genérico para que pylance reconozca bien los casos de los menúes de opciones
# (por eso esos usan list(enum) en vez de una lista normal y ya)
def choicer(opciones: list[T]) -> T:
    lngth = len(opciones)

    if lngth < 2:
        raise ValueError(f"Deben haber al menos dos opciones (hay {lngth})")
    while True:
        for i, o in enumerate(opciones):
            print(f"{i+1}. {o}")

        try:
            chi = int(input(f"\nElegí una opción [1-{lngth}]: ")) - 1
            if chi in range(0, lngth):
                return opciones[chi]
            else:
                clear()
                print(f"Opción inválida; Debés ingresar un número entre 1 y {lngth}\n")
        except ValueError:
            clear()
            print("Debés ingresar un número.")
