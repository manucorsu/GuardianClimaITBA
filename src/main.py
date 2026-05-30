from . import secrets
from .menus.acceso import menu_acceso
from .custom_types import OpcionesMenu
from .choicer import choicer
from .menus.consulta_clima import consulta_clima_prompt
from .menus.consultas_historial import historial_personal

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
    VER_HISTORIAL = "Ver historial de consultas"
    ESTADISTICAS_EXPORTAR = "Estadísticas de uso/exportar historial"
    IA_VESTIR = "Consejo IA: ¿Cómo me visto hoy?"
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
        case OpcMenuPrincipal.VER_HISTORIAL:
            historial_personal(username)
        case OpcMenuPrincipal.CERRAR_SESION:
            print()
            username = None
        case OpcMenuPrincipal.ACERCA_DE:
            texto = """
=== ACERCA DE GUARDIÁNCLIMA ITBA ===

GuardiánClima ITBA es una aplicación desarrollada en Python que permite consultar información climática en tiempo real, almacenar un historial global de consultas, generar estadísticas de uso y obtener recomendaciones de vestimenta mediante Inteligencia Artificial.
El objetivo del proyecto es integrar conceptos de Programación, Ciberseguridad, Análisis de Datos, Inteligencia Artificial y Conectividad mediante el uso de APIs externas y archivos CSV.

¿CÓMO UTILIZAR LA APLICACIÓN?

MENÚ DE ACCESO

1. Iniciar Sesión
   * El usuario ingresa su nombre de usuario y contraseña.
   * El sistema verifica las credenciales almacenadas en el archivo usuarios_simulados.csv.
   * Si los datos son correctos, se accede al menú principal.

2. Registrar Nuevo Usuario
   * El usuario elige un nombre de usuario disponible.
   * Luego crea una contraseña.
   * La contraseña es validada según criterios de seguridad definidos por el equipo.
   * Si no cumple los requisitos, el sistema informa los errores y brinda recomendaciones para mejorarla.
   * Si es válida, los datos se guardan en usuarios_simulados.csv y el usuario accede al menú principal.

3. Salir
   * Finaliza la ejecución de la aplicación.

MENÚ PRINCIPAL

1. Consultar Clima Actual
   * Permite consultar información meteorológica de una ciudad mediante la API OpenWeatherMap.
   * Los datos obtenidos se almacenan en historial_global.csv.

2. Ver Mi Historial Personal
   * Muestra las consultas realizadas por el usuario para una ciudad determinada.

3. Estadísticas Globales
   * Calcula la ciudad más consultada.
   * Muestra la cantidad total de consultas.
   * Calcula la temperatura promedio registrada.
   * Los datos almacenados pueden utilizarse posteriormente para generar gráficos en Excel.

4. Consejo IA: ¿Cómo Me Visto Hoy?
   * Utiliza la API Google Gemini.
   * A partir de los datos climáticos genera una recomendación breve y personalizada sobre vestimenta.

5. Acerca De...
   * Muestra información general del proyecto y su funcionamiento.

6. Cerrar Sesión
   * Finaliza la sesión actual y regresa al menú de acceso.

FUNCIONAMIENTO INTERNO

Gestión de Usuarios:
La aplicación utiliza un sistema simulado de usuarios almacenados en un archivo CSV. Durante el registro se verifica que las contraseñas cumplan criterios mínimos de seguridad, como longitud adecuada, uso de mayúsculas, minúsculas, números y caracteres especiales.

Importancia de las Contraseñas Seguras:
Las contraseñas robustas reducen el riesgo de accesos no autorizados y ayudan a proteger la información de los usuarios.

Advertencia de Seguridad:
El almacenamiento de contraseñas utilizado en este proyecto tiene fines exclusivamente educativos y no es seguro para aplicaciones reales. En sistemas profesionales se utilizan técnicas como hashing y salting para proteger las credenciales.

Obtención de Datos Climáticos:
La aplicación se conecta a la API de OpenWeatherMap para obtener información meteorológica actualizada en tiempo real.

Historial Global:
Cada consulta realizada se registra en historial_global.csv junto con la fecha, hora, usuario y datos climáticos.

Análisis de Datos:
A partir del historial global se generan estadísticas que permiten analizar tendencias y hábitos de uso. Además, los datos pueden exportarse y utilizarse para crear gráficos de barras, líneas y pie chart.

Inteligencia Artificial:
La aplicación utiliza Google Gemini para analizar las condiciones climáticas y generar recomendaciones prácticas de vestimenta mediante prompts diseñados por el equipo.


EQUIPO DE DESARROLLO

Nombre del grupo:
Los Meteorólogos del Teclado

Integrantes:
* Manuel Corsunsky Gayá
* Lautaro Cavagna
* Matias Barreiro
* Enzo Creatore

"""
            print(texto)
            input("\nPresiona Enter para volver al menú principal...")  
        case _:
            raise NotImplementedError()
