"""Páginas de checkout (datos personales, resumen y confirmación)."""

from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from utils.logger import log


class CheckoutPage(BasePage):
    CAMPO_NOMBRE = (By.ID, "first-name")
    CAMPO_APELLIDO = (By.ID, "last-name")
    CAMPO_POSTAL = (By.ID, "postal-code")
    BOTON_CONTINUAR = (By.ID, "continue")
    BOTON_FINALIZAR = (By.ID, "finish")
    TITULO = (By.CSS_SELECTOR, "span.title")
    MENSAJE_COMPLETO = (By.CLASS_NAME, "complete-header")

    def completar_datos(self, nombre: str, apellido: str, codigo_postal: str) -> None:
        log.info("Completar checkout: %s %s", nombre, apellido)
        self.escribir(self.CAMPO_NOMBRE, nombre)
        self.escribir(self.CAMPO_APELLIDO, apellido)
        self.escribir(self.CAMPO_POSTAL, codigo_postal)
        self.clic(self.BOTON_CONTINUAR)
        self.url_contiene("checkout-step-two")

    def finalizar(self) -> None:
        self.clic(self.BOTON_FINALIZAR)
        self.url_contiene("checkout-complete")

    def mensaje_compra_exitosa(self) -> str:
        return self.texto(self.MENSAJE_COMPLETO)
