"""Páginas de checkout (datos personales, resumen y confirmación)."""

from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from utils.logger import log


class CheckoutPage(BasePage):
    CAMPO_NOMBRE = (By.CSS_SELECTOR, "#first-name, [data-test='firstName']")
    CAMPO_APELLIDO = (By.CSS_SELECTOR, "#last-name, [data-test='lastName']")
    CAMPO_POSTAL = (By.CSS_SELECTOR, "#postal-code, [data-test='postalCode']")
    BOTON_CONTINUAR = (By.CSS_SELECTOR, "#continue, [data-test='continue']")
    BOTON_FINALIZAR = (By.CSS_SELECTOR, "#finish, [data-test='finish']")
    MENSAJE_COMPLETO = (By.CSS_SELECTOR, ".complete-header, [data-test='complete-header']")

    def completar_datos(self, nombre: str, apellido: str, codigo_postal: str) -> None:
        log.info("Completar checkout: %s %s", nombre, apellido)
        self.escribir(self.CAMPO_NOMBRE, nombre)
        self.escribir(self.CAMPO_APELLIDO, apellido)
        self.escribir(self.CAMPO_POSTAL, codigo_postal)
        self.clic(self.BOTON_CONTINUAR)
        self.url_contiene("checkout-step-two")

    def finalizar(self) -> None:
        self.clic(self.BOTON_FINALIZAR)
        self.encontrar_visible(self.MENSAJE_COMPLETO)

    def mensaje_compra_exitosa(self) -> str:
        return self.texto(self.MENSAJE_COMPLETO)
