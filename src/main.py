from .clear import clear
from . import secrets
from . import choicer
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
clear_menu_acceso = False
username = None
OPCIONES_MENU_ACCESO = ["Iniciar sesión", "Registrar nuevo usuario", "Salir"]
while username is None:
    if clear_menu_acceso:
        clear()
    else:
        clear_menu_acceso = True

    print("☀️  GuardianClimaITBA ☀️\n")

    print("🚪 Menú de acceso")
    choice = choicer.choicer(OPCIONES_MENU_ACCESO)
    match (choice):
        case 0:
            username = login_prompt()
        case 1:
            username = registrar_usuario_prompt()
            clear_menu_acceso = False
        case 2:
            print("Saliendo...")
            exit(0)
        case _:
            choicer.caso_imposible(choice, OPCIONES_MENU_ACCESO)
print(username)
