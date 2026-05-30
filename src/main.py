from . import secrets
from .menus.acceso import menu_acceso, login
from .custom_types import OpcionesMenu
from .choicer import choicer
from .menus.consulta_clima import consulta_clima_prompt
from .menus.consultas_historial import historial_personal, estadisticas_globales
from .menus.consulta_ia_vestir import prompt_ia_vestir
from .pause import pause
from .clear import clear
from pydoc import pager

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
    ESTADISTICAS_EXPORTAR = "Estadísticas globales, exportar historial global"
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
                print("✅.")
                historial_personal(username)
            except:
                print("❌ La contraseña es incorrecta.")
                pause()
                continue
            pause()
        case OpcMenuPrincipal.ESTADISTICAS_EXPORTAR:
            estadisticas_globales()
        case OpcMenuPrincipal.ACERCA_DE:
            texto = """
=== ACERCA DE GUARDIÁNCLIMA ITBA ===

GuardiánClima ITBA es una aplicación desarrollada en Python que permite consultar 
información climática en tiempo real, almacenar y procesar historial global de
consultas realizadas, generar estadísticas de uso y obtener recomendaciones de 
vestimenta mediante Inteligencia Artificial. El objetivo del proyecto es integrar
conceptos de Programación, Ciberseguridad, Análisis de Datos, Inteligencia 
Artificial y Conectividad/Cloud Computing mediante el uso de APIs externas y 
archivos CSV.

¿CÓMO UTILIZAR LA APLICACIÓN?

MENÚ DE ACCESO

1. Iniciar sesión
   * El usuario ingresa su nombre de usuario y contraseña.
   * El sistema verifica las credenciales almacenadas en el archivo 
     usuarios_simulados.csv.
   * Si los datos son correctos, se accede al menú principal.

2. Registrar nuevo usuario
   * El usuario elige un nombre de usuario disponible.
   * Luego crea una contraseña.
   * La contraseña es validada según criterios de seguridad definidos por el 
     equipo basados en lo visto en el Módulo de Ciberseguridad:
        * longitud: No puede tener menos de 12 caracteres.
        * contenido: No puede contener el nombre de usuario, ser una 
          contraseña común, contener el año actual o palabras relacionadas al clima o
          a la aplicación.
        * complejidad: Debe mezclar diferentes tipos de caracteres
          (mayúsculas, minúsculas, números y símbolos).

   * Si no cumple los requisitos, el sistema informa los errores y brinda 
     recomendaciones para mejorarla.
   * Si es válida, los datos se guardan en usuarios_simulados.csv y el usuario 
     accede al Menú Principal.

3. Salir de la aplicación
   * Finaliza la ejecución de la aplicación.

MENÚ PRINCIPAL

1. Consultar clima actual
   * Permite consultar información meteorológica de una ciudad mediante la API 
     OpenWeatherMap.
   * Los datos obtenidos se almacenan en historial_global.csv.

2. Ver mi historial personal de consultas
   * Muestra las consultas realizadas por el usuario para una ciudad determinada.
   * En cumplimiento con lo que pide la consigna de hacer que
     una funcionalidad sea "password-protected", esta es esa funcionalidad:
     no se permite su uso sin que antes el usuario reingrese correctamente su
     contraseña 

3. Estadísticas globales y exportar historial global
   * Primero, calcula y muestra los siguientes datos:
      * ciudad más consultada.
      * cantidad total de consultas.
      * temperatura promedio registrada.
   * Luego, exporta el historial global actual para que este pueda ser interpretado
     y sus datos graficados por el usuario en una aplicación como Excel.

4. Consejo IA: ¿Cómo me visto hoy?
   * Utiliza la API de Google Gemini.
   * A partir de los datos climáticos de la última consulta realizada por el 
     usuario, genera una recomendación breve y personalizada sobre vestimenta.

5. Acerca de...
   * Muestra información general del proyecto y su funcionamiento.
   * Es lo que están leyendo actualmente.

6. Cerrar sesión
   * Finaliza la sesión actual y regresa al Menú de Acceso.

FUNCIONAMIENTO INTERNO

Gestión de usuarios:
La aplicación utiliza un sistema simulado de usuarios almacenados en un archivo
CSV. Durante el registro se verifica que las contraseñas cumplan criterios mínimos 
de seguridad (ver sección del Menú de Acceso para más info.)

Importancia de las contraseñas seguras:
Las contraseñas robustas reducen el riesgo de accesos no autorizados y 
ayudan a proteger la información de los usuarios. Es por eso que implementamos
los requerimientos que implementamos en línea con lo recomendado en el Módulo
de Ciberseguridad.

Advertencia de seguridad:
El almacenamiento de contraseñas utilizado en este proyecto tiene fines
exclusivamente educativos y no es seguro para aplicaciones reales. En sistemas
profesionales se utilizan técnicas como hashing y salting para proteger las
credenciales. El sistema que usa este trabajo para guardar las contraseñas,
un simple CSV de par `usuario,contraseña en texto plano` es extremadamente 
inseguro y nunca debería utilizarse para ningún proyecto real, solo lo hacemos
porque así lo solicita la consigna.

Obtención de datos climáticos:
La aplicación se conecta a la API de OpenWeatherMap para obtener información
meteorológica actualizada en tiempo real. Debido a que decidimos utilizar el
método actual recomendado por OWM en vez del sugerido por la consigna (ver
aclaración en src/geo/owm.py), esto implica primero contactar a su API de
Geocoding para obtener las coordenadas de la ciudad a partir de su nombre,
(las cuales son cacheadas en un simple cache en JSON para evitar requests
excesivas), para recién ahí poder solicitar a la Current Weather API el clima
en esas coordenadas.

Historial global:
Cada consulta realizada se registra en historial_global.csv junto con la 
fecha, hora, usuario y datos climáticos (temperatura, sensación térmica,
condición climática según la descripción de OWM, porcentaje de humedad y 
velocidad del viento)

Análisis de datos:
A partir del historial global, el cual puede ser fácilmente exportado a CSV,
el usuario utiliza herramientas como Excel para encontrar y graficar tendencias y
hábitos de uso.

Inteligencia artificial:
La aplicación utiliza Google Gemini para analizar las condiciones climáticas y
generar recomendaciones prácticas de vestimenta mediante un prompt diseñado por el
equipo en base a la última solicitud hecha por el usuario


EQUIPO DE DESARROLLO

Nombre del grupo:
"Los Meteorólogos del Teclado"

Integrantes:
* Manuel Corsunsky Gayá
* Lautaro Cavagna
* Matías Barreiro
* Enzo Creatore
"""
            pager(texto)
        case OpcMenuPrincipal.IA_VESTIR:
            prompt_ia_vestir(username)
            pause()
        case OpcMenuPrincipal.CERRAR_SESION:
            print()
            username = None
    clear()
