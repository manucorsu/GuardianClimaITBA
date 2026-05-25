from . import secrets

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
