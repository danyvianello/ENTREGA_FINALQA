"""Rutas del repositorio usadas por configuración, reportes y datos."""

from pathlib import Path

RAIZ_PROYECTO = Path(__file__).resolve().parent.parent
RUTA_DATOS = RAIZ_PROYECTO / "datos"
RUTA_REPORTES = RAIZ_PROYECTO / "reports"
RUTA_CAPTURAS = RUTA_REPORTES / "capturas"
RUTA_LOGS = RUTA_REPORTES / "logs"
