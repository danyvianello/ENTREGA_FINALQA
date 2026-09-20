"""Configuración de logging para seguir los pasos de cada prueba."""

import logging
from datetime import datetime

from utils.rutas import RUTA_LOGS

NOMBRE_LOGGER = "framework_qa"


def configurar_logging() -> logging.Logger:
    """Crea el logger del framework (consola + archivo diario en reports/logs)."""
    RUTA_LOGS.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger(NOMBRE_LOGGER)
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)
    formato = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")

    archivo = RUTA_LOGS / f"ejecucion_{datetime.now().strftime('%Y%m%d')}.log"
    handler_archivo = logging.FileHandler(archivo, encoding="utf-8")
    handler_archivo.setFormatter(formato)

    handler_consola = logging.StreamHandler()
    handler_consola.setFormatter(formato)

    logger.addHandler(handler_archivo)
    logger.addHandler(handler_consola)
    logger.propagate = False
    return logger


log = configurar_logging()
