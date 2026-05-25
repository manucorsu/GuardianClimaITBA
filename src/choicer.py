def choicer(opciones: list[str], mensaje: str = "Elegí una opción") -> int:
    lngth = len(opciones)
    if lngth < 2:
        raise ValueError("Deben haber por lo menos dos opciones.")

    mensaje += f" [1-{lngth}]"
    while True:
        print(mensaje)
        for i, opcion in enumerate(opciones):
            print(f"{i+1}. {opcion}")
        try:
            eleccion = int(input("Opción: "))
            if 1 <= eleccion <= lngth:
                return eleccion
            else:
                print(f"Por favor, ingresá un número entre 1 y {lngth}.")
        except ValueError:
            print("Entrada no válida. Por favor, ingresá un número.")
