# Ver aclaración sobre por qué no usamos google.generativeai
# en requirements.txt
from google import genai
from .custom_types import Clima
from .secrets import gemini_api_key
from .pause import pause

assert gemini_api_key is not None

print("Inicializando el cliente de Gemini...", end="")


PROMPT = "Estoy en {} y por salir. El clima se describe como {}, la sensación térmica es {}°C, la humedad {}% y la velocidad del viento {} km/h. ¿Qué debería ponerme? Sé breve y práctico."


# Mezclando el método de la consigna con el actual:
# https://github.com/googleapis/python-genai
def obtener_consejo_ia_gemini(c: Clima):
    print("Inicialiando el cliente de Gemini...", end="")
    client = None
    try:
        client = genai.Client(api_key=gemini_api_key)
        print(" ✅.")
    except Exception as ex:
        print(
            f"❌. Ocurrió un error al intentar establecer el cliente de Gemini. Verificá que la GEMINI_API_KEY en .env sea correcta. Las funciones de Gemini no estarán disponibles. Error:\n{ex}"
        )
        pause()
        return

    print("✨ Obteniendo el consejo de Gemini...", end="")

    fp = PROMPT.format(
        c["Ciudad"],
        c["Condicion_Clima"],
        c["Sensacion_Termica"],
        c["Humedad_Porcentaje"],
        c["Viento_kmh"],
    )
    try:
        response = (
            client.models.generate_content(  # pyright: ignore[reportUnknownMemberType]
                model="gemini-2.5-flash",
                contents=fp,
                config={
                    "temperature": 0.05,
                    "top_p": 0.95,
                    "top_k": 20,
                },
            )
        )
        resultado = response.text
        if resultado is None:
            raise ValueError("Gemini no devolvió un resultado.")
        print(" ✅.")
        return resultado
    except Exception as ex:
        print(f"❌. Ocurrió un error: {ex}")
        pause()
