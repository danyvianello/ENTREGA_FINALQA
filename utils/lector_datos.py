"""Lectura de datos de prueba desde CSV y JSON (parametrización externa)."""

import csv
import json
from pathlib import Path

from utils.rutas import RUTA_DATOS


def leer_json(nombre_archivo: str) -> dict:
    """Carga un archivo JSON ubicado en /datos."""
    ruta = RUTA_DATOS / nombre_archivo
    with ruta.open(encoding="utf-8") as archivo:
        return json.load(archivo)


def leer_csv(nombre_archivo: str) -> list[dict]:
    """Carga un CSV de /datos y devuelve una lista de diccionarios."""
    ruta: Path = RUTA_DATOS / nombre_archivo
    with ruta.open(encoding="utf-8", newline="") as archivo:
        return list(csv.DictReader(archivo))


def casos_login_por_escenario(escenario: str) -> list[dict]:
    """Filtra las filas de login.csv por tipo de escenario."""
    return [fila for fila in leer_csv("login.csv") if fila["escenario"] == escenario]


def nombres_productos() -> list[str]:
    """Lista de productos a usar en tests parametrizados."""
    return [fila["nombre_producto"] for fila in leer_csv("productos.csv")]
