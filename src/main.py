from .clear import clear
from . import secrets
from .opc_menu_base import OpcionesMenu
from .choicer import choicer
from .acceso import login_prompt, registrar_usuario_prompt

print("☀️  Iniciando GuardianClimaITBA ☀️")

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


# entrypoint: Menú de Acceso
class OpcMenuAcceso(OpcionesMenu):
    INICIAR_SESION = "Iniciar sesión"
    REGISTRAR_USUARIO = "Registrar nuevo usuario"
    SALIR = "Salir de la aplicación"


clear_menu_acceso = False
username = None
while username is None:
    if clear_menu_acceso:
        clear()
    else:
        clear_menu_acceso = True

    print("☀️  GuardianClimaITBA ☀️\n")
    print("🚪 Menú de acceso")
    ch = choicer(list(OpcMenuAcceso))
    match (ch):
        case OpcMenuAcceso.INICIAR_SESION:
            username = login_prompt()
        case OpcMenuAcceso.REGISTRAR_USUARIO:
            username = registrar_usuario_prompt()
            clear_menu_acceso = False
        case OpcMenuAcceso.SALIR:
            print("Saliendo...")
            exit(0)
print(username)
