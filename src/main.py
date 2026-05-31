from . import secrets
from .menus.acceso import menu_acceso, login
from .custom_types import OpcionesMenu
from .choicer import choicer
from .menus.consulta_clima import consulta_clima_prompt
from .menus.consultas_historial import historial_personal, estadisticas_globales
from .menus.consulta_ia_vestir import prompt_ia_vestir
from .menus.acerca_de import acerca_de
from .pause import pause, pause_and_clear
from .clear import clear

clear()

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
    CONSULTA_CLIMA = "Consultar clima actual"  # (y guardar en historial global)
    VER_HISTORIAL = "Ver mi historial personal de consultas 🔒️"
    ESTADISTICAS_EXPORTAR = "Estadísticas globales y exportar historial global"
    IA_VESTIR = "Consejo IA: ¿Cómo me visto hoy? 🤖"
    ACERCA_DE = "Acerca de"
    CERRAR_SESION = "Cerrar sesión"


username = None
while True:
    # entrypoint: Menú de Acceso
    if username is None:
        username = menu_acceso()

    # Una vez autenticado pasa al menú principal
    print("☀️  GuardiánClima ITBA ☀️\n")
    print("📜 Menú principal\n")
    ch = choicer(list(OpcMenuPrincipal))
    match (ch):
        case OpcMenuPrincipal.CONSULTA_CLIMA:
            consulta_clima_prompt(username)
            pause()
        case OpcMenuPrincipal.VER_HISTORIAL:
            clear()
            try:
                login(
                    username,
                    input(
                        "🔒️ Debés ingresar tu contraseña para acceder al historial: "
                    ),
                )
                clear()
                print("✅ Se verificó con éxito.")
                historial_personal(username)
            except:
                print("❌ La contraseña es incorrecta.")
                pause_and_clear()
                continue
            pause()
        case OpcMenuPrincipal.ESTADISTICAS_EXPORTAR:
            estadisticas_globales()
        case OpcMenuPrincipal.ACERCA_DE:
            acerca_de()
        case OpcMenuPrincipal.IA_VESTIR:
            prompt_ia_vestir(username)
            pause()
        case OpcMenuPrincipal.CERRAR_SESION:
            print()
            username = None
    clear()
