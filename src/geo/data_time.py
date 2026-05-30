from typing import Any
from datetime import datetime, timedelta, timezone


# Consolida la `dt` y `timezone` de las respuestas que da OWM
# a un solo datetime.datetime
def api_dt_to_datetime(dt: Any, timezone_api: Any):
    offset = timezone(timedelta(seconds=float(timezone_api)))
    return datetime.fromtimestamp(float(dt), offset)


MESES = (
    "enero",
    "febrero",
    "marzo",
    "abril",
    "mayo",
    "junio",
    "julio",
    "agosto",
    "septiembre",
    "octubre",
    "noviembre",
    "diciembre",
)


def pretty_dt(dt: datetime):
    if dt.tzinfo is None or dt.utcoffset() is None:
        raise ValueError("El datetime debe ser offset-aware")
    return f"{dt.day} de {MESES[dt.month - 1]} de {dt.year} " f"a las {dt:%H:%M}"
