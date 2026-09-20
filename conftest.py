"""Fixtures globales: navegador por test, login y capturas en el reporte HTML."""

from datetime import datetime
from pathlib import Path

import pytest
from pytest_html import extras

from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from utils.driver_factory import crear_driver
from utils.lector_datos import casos_login_por_escenario
from utils.logger import log
from utils.rutas import RUTA_CAPTURAS, RUTA_LOGS, RUTA_REPORTES


def pytest_configure(config):
    RUTA_REPORTES.mkdir(parents=True, exist_ok=True)
    RUTA_CAPTURAS.mkdir(parents=True, exist_ok=True)
    RUTA_LOGS.mkdir(parents=True, exist_ok=True)


@pytest.fixture
def navegador():
    """Un Chrome nuevo por test: si uno falla, el siguiente arranca limpio."""
    driver = crear_driver()
    yield driver
    driver.quit()
    log.info("Navegador cerrado")


@pytest.fixture
def sesion_logueada(navegador):
    """Abre Sauce Demo ya autenticado con el usuario válido del CSV."""
    credenciales = casos_login_por_escenario("valido")[0]
    login = LoginPage(navegador)
    login.abrir()
    login.iniciar_sesion(credenciales["usuario"], credenciales["contrasena"])
    inventario = InventoryPage(navegador)
    inventario.url_contiene("/inventory.html")
    return navegador


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Ante un fallo de UI, guarda PNG y lo adjunta al reporte HTML."""
    outcome = yield
    reporte = outcome.get_result()
    extras_html = getattr(reporte, "extras", [])

    if reporte.when == "call" and reporte.failed:
        driver = item.funcargs.get("navegador") or item.funcargs.get("sesion_logueada")
        if driver is not None:
            marca = datetime.now().strftime("%Y%m%d-%H%M%S")
            nombre = item.name.replace("/", "_").replace("[", "_").replace("]", "_")
            archivo = Path(RUTA_CAPTURAS) / f"{nombre}_{marca}.png"
            driver.save_screenshot(str(archivo))
            log.error("Captura de fallo: %s | URL=%s", archivo, driver.current_url)
            extras_html.append(extras.png(str(archivo)))
            extras_html.append(extras.text(f"Captura: {archivo.name}"))

    reporte.extras = extras_html
