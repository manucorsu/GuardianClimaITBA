# ☀️ GuardiánClima ITBA

**Grupo 121 ("Los Meteorólogos del Teclado")**

- Matías Barreiro
- Lautaro Cavagna
- Manuel Corsunsky Gayá
- Enzo Creatore
<!--TODO: legajos?-->

## 1. Instrucciones de instalación

- Se requiere que el sistema tenga **Python 3.11 o superior instalado**. Este programa fue probado principalmente en la última versión estable de Python, 3.14.5, y funciona perfectamente en ella.
- Se mostrarán varios comandos a ejecutar en la terminal. Tener en cuenta:
  - Los comandos deben ser ejecutados **en el directorio del proyecto** y en una terminal válida:
    - **cmd** en Windows (las instrucciones están escritas exclusivamente para cmd y no para PowerShell)
    - **zsh, bash o similar** en macOS y Linux.
  - _**importante para usuarios de macOS y Linux**: Las instrucciones muestran al comando de Python como `python`. Dependiendo de su configuración, puede que tengan que cambiarlo por `python3` u otra variación. El mismo comando que usen habitualmente debería estar bien siempre y cuando este corresponda a una versión de Python estándar, estable y mayor a 3.11_

### 1.1 Crear el entorno virtual

Usamos los entornos virtuales de Python (`venv`) para evitar conflictos entre los paquetes que descarga nuestra aplicación y los que ya pudieran estar instalados en el sistema.

Para crear un entorno virtual **en Windows**, ejecutar:

```cmd
python -m venv .venv
```

En **macOS y Linux es igual**, solo deben cambiar `python` por `python3` o el comando que corresponda.

Deberían ver que en el directorio del proyecto se creó un directorio `.venv`, si no lo ven, verifiquen haber ejecutado el comando correctamente.

### 1.2 Habilitar el venv

> **Importante:** Se debe realizar este paso **cada vez que se abra una terminal nueva** para utilizar la aplicación. En todo momento debería aparecer (.venv) antes de ejecutar la apliación. (Todo el resto de los pasos de esta sección son requeridos únicamente la primera vez que se abre)

En **Windows**, ejecutar:

```cmd
call .venv\Scripts\Activate
```

En **macOS y Linux**:

```bash
source .venv/bin/activate
```

En cualquier caso, deberían ver **`(.venv)`** escrito al lado del campo en el que normalmente escriben los comandos en la terminal, ej. (en Windows):

![(.venv) C:\Users\user\GuardiánClima ITBA>](./assets/venv.png)

### 1.3 Instalar las dependencias

Todas las dependencias están en `requirements.txt`, en un formato que permite que pip las instale con un solo comando. En cualquier plataforma:

```bash
python -m pip install -r requirements.txt
```

Verán cómo pip descarga todas las dependencias (y sus dependencias) al venv, puede tardar un tiempo. Si ven un error, asegúrense de tener el entorno activado y estar utilizando una versión de Python mayor o igual a 3.11.

### 1.4 Crear `.env` con las API Keys necesarias.

El `.env` (no confundir con `.venv`) es un archivo de texto que contiene las API keys y otros datos sensibles que no deben ser subidos como parte del repositorio. Por este motivo, no aparece creado, ya que está en `.gitignore`.

Para que el programa pueda utilizar las APIs de OpenWeatherMap y Gemini, deben crear manualmente un archivo de texto **en el root del proyecto** y llamarlo `.env` (asegúrense de que no haya nada antes del punto ni después de `env`, el nombre completo del archivo debe ser `.env`, no `.env.txt` ni nada parecido), y en él, escriban estas dos líneas:

```dotenv
OWM_API_KEY='tu api key de OWM'
GEMINI_API_KEY='tu api key de Gemini'
```

Reemplazando `'tu api key de de OWM'` y `'tu api key de Gemini'` por sus keys reales de OpenWeatherMap y Gemini respectivamente.

Si no tienen alguna o ambas de las dos API Keys solicitadas, se pueden obtener de forma gratuita en:
- **OpenWeatherMap**: [https://openweathermap.org/](https://openweathermap.org/)
- **Gemini**: [https://aistudio.google.com/](https://aistudio.google.com/)

**El programa no funcionará si no están ambas keys presentes al momento de ejecutarlo, se cerrará con un error indicando que falta una API Key.**

### 1.5 Correr la aplicación

Simplemente ejecuten en una terminal con el venv actviado:

```bash
python -m src.main
```

Y cualquier otro archivo requerido (ej. los CSVs solicitados vacíos), será creado automáticamente por la aplicación.

Esta sintaxis (con `-m` y `src.main` en vez de `python src/main.py` por ejemplo) se utiliza porque la aplicación está dividida en módulos.

# 2. Flujo de menús

Al iniciar la aplicación, lo primero que se ve es el **Menú de Acceso**.

## 2.1 Menú de Acceso

En el Menú de Acceso, el usuario se registra o inicia sesión a su cuenta ya existente, paso necesario para acceder a las funcionalidades de la aplicación en el Menú Principal

1. **Iniciar sesión**
   - El usuario ingresa su nombre de usuario y contraseña.
   - El sistema verifica las credenciales almacenadas en el archivo
     usuarios_simulados.csv.
   - Si los datos son correctos, se accede al menú principal.

2. **Registrar nuevo usuario**
   - El usuario elige un nombre de usuario disponible.
   - Luego crea una contraseña.
   - La contraseña es validada según criterios de seguridad definidos por el
     equipo basados en lo visto en el Módulo de Ciberseguridad:
     - longitud: No puede tener menos de 12 caracteres.
     - contenido: No puede contener el nombre de usuario, ser una
       contraseña común, contener el año actual o palabras relacionadas al clima o
       a la aplicación.
     - complejidad: Debe mezclar diferentes tipos de caracteres
       (mayúsculas, minúsculas, números y símbolos).

   - Si no cumple los requisitos, el sistema informa los errores y brinda
     recomendaciones para mejorarla.
   - Si es válida, los datos se guardan en usuarios_simulados.csv y el usuario
     accede al Menú Principal.
   - En cumplimiento con la consigna, las contraseñas no están encriptadas, algo que es extremadamente inseguro y solo se acepta debido a que es un proyecto introductorio y educativo.

3. **Salir de la aplicación**
   - Finaliza la ejecución de la aplicación.

## 2.2 Menú principal

Una vez que el usuario se registra o inicia sección exitosamente, accede al menú principal, desde el cual se accede a todo el resto de las funcionalidades de la aplicación:

1. **Consultar clima actual**
   - Permite consultar información meteorológica de una ciudad mediante la API
     OpenWeatherMap.
   - Los datos obtenidos se almacenan en historial_global.csv.

2. **Ver mi historial personal de consultas**
   - Muestra las consultas realizadas por el usuario para una ciudad determinada.
   - En cumplimiento con lo que pide la consigna de hacer que
     una funcionalidad sea "password-protected", esta es esa funcionalidad:
     no se permite su uso sin que antes el usuario reingrese correctamente su
     contraseña

3. **Estadísticas globales y exportar historial global**
   - Primero, calcula y muestra los siguientes datos:
     - ciudad más consultada.
     - cantidad total de consultas.
     - temperatura promedio registrada.
   - Luego, exporta el historial global actual para que este pueda ser interpretado
     y sus datos graficados por el usuario en una aplicación como Excel.

4. **Consejo IA: ¿Cómo me visto hoy?**
   - Utiliza la API de Google Gemini.
   - A partir de los datos climáticos de la última consulta realizada por el
     usuario, genera una recomendación breve y personalizada sobre vestimenta.

5. **Acerca de...**
   - Muestra información general del proyecto y su funcionamiento.
   - Es lo que están leyendo actualmente.

6. **Cerrar sesión**
   - Finaliza la sesión actual y regresa al Menú de Acceso.
