"""Fábrica de WebDriver (Chrome) para las pruebas de UI."""

import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from utils.logger import log


def crear_driver() -> webdriver.Chrome:
    """
    Abre Chrome para un test.

    HEADLESS=1 ejecuta sin ventana (CI o servidor sin escritorio).
    """
    opciones = Options()
    opciones.add_argument("--window-size=1280,800")
    opciones.add_argument("--disable-gpu")
    opciones.add_argument("--no-sandbox")
    opciones.add_argument("--disable-dev-shm-usage")

    if os.getenv("HEADLESS", "").strip().lower() in {"1", "true", "yes"}:
        opciones.add_argument("--headless=new")
        log.info("Chrome iniciado en modo headless")
    else:
        log.info("Chrome iniciado en modo visible")

    driver = webdriver.Chrome(options=opciones)
    driver.implicitly_wait(0)
    return driver
