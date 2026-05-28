import csv
from typing import Any
from pathlib import Path


def leer_o_crear(path: str, columnas: list[str]) -> list[dict[str, str]]:
    try:
        with open(path, "r", newline="") as f:
            reader = csv.DictReader(f)

            if reader.fieldnames != columnas:
                raise ValueError(
                    f"Las columnas del CSV no coinciden con las esperadas. Se esperaba {columnas}, pero se encontró {reader.fieldnames}"
                )

            return list(reader)

    except FileNotFoundError:
        escribir(path, columnas, [])


def escribir(path: str, columnas: list[str], datos: list[dict[str, Any]]):
    Path(path).parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=columnas)
        writer.writeheader()
        writer.writerows(datos)
