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


def pretty_dt(dt: datetime, reverse: bool = False):
    offset = dt.utcoffset()
    if dt.tzinfo is None or offset is None:
        raise ValueError("El datetime debe ser offset-aware")

    total_minutes = int(offset.total_seconds() // 60)
    sign = "+" if total_minutes >= 0 else "-"
    abs_minutes = abs(total_minutes)
    hours = abs_minutes // 60
    minutes = abs_minutes % 60
    utc_offset = (
        f"UTC{sign}{hours}" if minutes == 0 else f"UTC{sign}{hours}:{minutes:02d}"
    )

    dmy = f"{dt.day} de {MESES[dt.month - 1]} de {dt.year}"
    hhmm = f"a las {dt:%H:%M} hora local ({utc_offset})"
    return hhmm + " del " + dmy if reverse else dmy + " " + hhmm
