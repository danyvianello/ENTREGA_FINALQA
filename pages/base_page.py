"""Page Object base: esperas explícitas y acciones comunes."""

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from utils.logger import log

TIMEOUT_EXPLICITO = 10


class BasePage:
    """Encapsula interacciones de Selenium para que las páginas no repitan código."""

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(driver, TIMEOUT_EXPLICITO)

    def visitar(self, url: str) -> None:
        log.info("Navegar a %s", url)
        self.driver.get(url)

    def encontrar_visible(self, locator: tuple) -> WebElement:
        return self.wait.until(EC.visibility_of_element_located(locator))

    def encontrar_clicable(self, locator: tuple) -> WebElement:
        return self.wait.until(EC.element_to_be_clickable(locator))

    def escribir(self, locator: tuple, texto: str) -> None:
        campo = self.encontrar_visible(locator)
        campo.clear()
        campo.send_keys(texto)
        log.info("Escribir en %s: %s", locator[1], texto)

    def clic(self, locator: tuple) -> None:
        self.encontrar_clicable(locator).click()
        log.info("Clic en %s", locator[1])

    def texto(self, locator: tuple) -> str:
        return self.encontrar_visible(locator).text

    def url_contiene(self, fragmento: str) -> bool:
        return self.wait.until(EC.url_contains(fragmento))
