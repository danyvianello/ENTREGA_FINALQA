"""Página de inventario / catálogo."""

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage
from utils.logger import log


class InventoryPage(BasePage):
    TITULO = (By.CSS_SELECTOR, "span.title, [data-test='title']")
    LOGO = (By.CLASS_NAME, "app_logo")
    ITEMS = (By.CSS_SELECTOR, ".inventory_item, [data-test='inventory-item']")
    BOTON_MENU = (By.ID, "react-burger-menu-btn")
    ENLACE_LOGOUT = (By.CSS_SELECTOR, "#logout_sidebar_link, [data-test='logout-sidebar-link']")
    TEXTO_LOGOUT = (By.LINK_TEXT, "Logout")
    FILTRO = (By.CSS_SELECTOR, ".product_sort_container, [data-test='product-sort-container']")
    BADGE_CARRITO = (By.CSS_SELECTOR, ".shopping_cart_badge, [data-test='shopping-cart-badge']")
    ENLACE_CARRITO = (By.CSS_SELECTOR, ".shopping_cart_link, [data-test='shopping-cart-link']")
    BOTON_CHECKOUT = (By.CSS_SELECTOR, "#checkout, [data-test='checkout']")
    CAMPO_USUARIO = (By.ID, "user-name")

    def titulo_visible(self) -> str:
        return self.texto(self.TITULO)

    def logo_visible(self) -> str:
        return self.texto(self.LOGO)

    def cantidad_productos(self) -> int:
        self.encontrar_visible(self.ITEMS)
        return len(self.driver.find_elements(*self.ITEMS))

    def menu_y_filtro_visibles(self) -> None:
        self.encontrar_visible(self.BOTON_MENU)
        self.encontrar_visible(self.FILTRO)

    def agregar_producto(self, nombre_producto: str) -> None:
        boton = (
            By.XPATH,
            "//div[contains(@class,'inventory_item') or @data-test='inventory-item']"
            f"[.//div[normalize-space()='{nombre_producto}']]"
            "//button[contains(@class,'btn_inventory') or contains(@data-test,'add-to-cart')]",
        )
        log.info("Agregar al carrito: %s", nombre_producto)
        self.clic(boton)

    def contador_carrito(self) -> str:
        return self.texto(self.BADGE_CARRITO)

    def ir_al_carrito(self) -> None:
        self.clic(self.ENLACE_CARRITO)
        self.wait.until(
            lambda driver: "/cart" in driver.current_url
            or bool(driver.find_elements(*self.BOTON_CHECKOUT))
        )
        log.info("Carrito visible. URL=%s", self.driver.current_url)

    def cerrar_sesion(self) -> None:
        self.clic(self.BOTON_MENU)
        logout = self.wait.until(EC.visibility_of_element_located(self.TEXTO_LOGOUT))
        self.driver.execute_script("arguments[0].click();", logout)
        log.info("Clic JS en Logout")
        self.wait.until(EC.visibility_of_element_located(self.CAMPO_USUARIO))
        log.info("Logout completado. URL=%s", self.driver.current_url)
