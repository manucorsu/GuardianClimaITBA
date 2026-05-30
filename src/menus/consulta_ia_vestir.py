from ..historial import obtener_ultima_consulta
from ..ai import obtener_consejo_ia_gemini
from ..custom_types import pretty_dt


def prompt_ia_vestir(username: str):
    ultima_consulta = obtener_ultima_consulta(username)
    if ultima_consulta is None:
        print(
            "Debés hacer una consulta de clima para que la IA hacer su recomendación."
        )
        return
    dt = pretty_dt(ultima_consulta["FechaHoraCompleta"], reverse=True)
    print(
        f"Se le consultará a Gemini cómo deberías vestirte en {ultima_consulta["Ciudad"]} si el clima está como estaba {dt} (tu última consulta)."
    )
    # Ej. "Se le consultará a Gemini cómo deberías vestirte en Buenos Aires, AR a las 02:19 hora local (UTC-3) del 30 de mayo de 2026."
    consejo = obtener_consejo_ia_gemini(ultima_consulta)
    if consejo is None:
        return
    print(f"✨ Gemini dice:\n{consejo}")
