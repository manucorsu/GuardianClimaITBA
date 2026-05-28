from . import secrets
from .menus.acceso import menu_acceso
from .menus.opc_menu_base import OpcionesMenu
from .choicer import choicer

print("☀️  Iniciando GuardiánClima ITBA ☀️")

# No se permite la ejecución si no están las keys
print("Validando existencia de API keys... ", end="")
if not secrets.owm_api_key:
    print(
        "❌\nAPI key de OpenWeatherMap no encontrada. Asegurate de tener un archivo .env creado en el root del proyecto con la variable OWM_API_KEY asignada."
    )
    exit(1)
if not secrets.gemini_api_key:
    print(
        "❌\nAPI key de Gemini no encontrada. Asegurate de tener un archivo .env creado en el root del proyecto con la variable GEMINI_API_KEY asignada."
    )
    exit(1)
print("✅\n")

class OpcMenuPrincipal(OpcionesMenu):
    CONSULTA_CLIMA = "Consultar clima actual" # (y guardar en historial global)
    VER_HISTORIAL = "Ver historial de consultas"
    ESTADISTICAS_EXPORTAR = "Estadísticas de uso/exportar historial"
    IA_VESTIR = "Consejo IA: ¿Cómo me visto hoy?"
    ACERCA_DE = "Acerca de"
username = None
while True:
    # entrypoint: Menú de Acceso
    if username is None:
        username = menu_acceso()

    # Una vez autenticado pasa al menú principal
    print("☀️  GuardiánClima ITBA ☀️\n")
    print("📜 Menú principal\n")
    ch = choicer(list(OpcMenuPrincipal))
    raise NotImplementedError()
