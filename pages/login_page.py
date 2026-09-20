"""Página de login de Sauce Demo."""

from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from utils.logger import log

URL_LOGIN = "https://www.saucedemo.com"


class LoginPage(BasePage):
    CAMPO_USUARIO = (By.ID, "user-name")
    CAMPO_CONTRASENA = (By.ID, "password")
    BOTON_LOGIN = (By.ID, "login-button")
    MENSAJE_ERROR = (By.CSS_SELECTOR, "h3[data-test='error']")

    def abrir(self) -> None:
        self.visitar(URL_LOGIN)
        self.encontrar_visible(self.CAMPO_USUARIO)

    def iniciar_sesion(self, usuario: str, contrasena: str) -> None:
        log.info("Intentar login con usuario=%s", usuario)
        self.escribir(self.CAMPO_USUARIO, usuario)
        self.escribir(self.CAMPO_CONTRASENA, contrasena)
        self.clic(self.BOTON_LOGIN)

    def mensaje_de_error(self) -> str:
        return self.texto(self.MENSAJE_ERROR)
