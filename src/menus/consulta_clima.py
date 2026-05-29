from ..geo.owm import geocode_nombre_ciudad


def consulta_clima_prompt():
    print(
        "💡 Consejo: para obtener mejores resultados, escribí el nombre de la ciudad junto con su código de país, ej: 'Buenos Aires, AR' o 'París, FR'"
    )
    ciudad = input("Ingresa el nombre de una ciudad: ")
    print(geocode_nombre_ciudad(ciudad))
