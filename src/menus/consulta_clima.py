from ..geo import owm
from ..custom_types import pretty_print_informe


def consulta_clima_prompt(username: str):
    print(
        "\n--CONSULTAR CLIMA--\n💡 Consejo: para obtener mejores resultados, escribí el nombre de la ciudad junto con su código de país, ej: 'Buenos Aires, AR' o 'París, FR'"
    )

    ciudad = None
    while ciudad is None:
        ciudad = owm.geocode_nombre_ciudad(input("\nIngresa el nombre de una ciudad: "))
    clima = owm.buscar_clima(username, ciudad)  # type: ignore[reportAttributeAccessIssue, reportUnknownMemberType]
    if clima is None:
        return  # Vuelve al inicio
    pretty_print_informe(clima)
