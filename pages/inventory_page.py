"""Página de inventario / catálogo."""

from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from utils.logger import log


class InventoryPage(BasePage):
    TITULO = (By.CSS_SELECTOR, "span.title")
    LOGO = (By.CLASS_NAME, "app_logo")
    ITEMS = (By.CLASS_NAME, "inventory_item")
    BOTON_MENU = (By.ID, "react-burger-menu-btn")
    ENLACE_LOGOUT = (By.ID, "logout_sidebar_link")
    FILTRO = (By.CLASS_NAME, "product_sort_container")
    BADGE_CARRITO = (By.CLASS_NAME, "shopping_cart_badge")
    ENLACE_CARRITO = (By.CLASS_NAME, "shopping_cart_link")

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
            f"//div[@class='inventory_item' and .//div[text()='{nombre_producto}']]"
            "//button[contains(@class,'btn_inventory')]",
        )
        log.info("Agregar al carrito: %s", nombre_producto)
        self.clic(boton)

    def contador_carrito(self) -> str:
        return self.texto(self.BADGE_CARRITO)

    def ir_al_carrito(self) -> None:
        self.clic(self.ENLACE_CARRITO)
        self.url_contiene("/cart.html")

    def cerrar_sesion(self) -> None:
        self.clic(self.BOTON_MENU)
        self.clic(self.ENLACE_LOGOUT)
        self.url_contiene("saucedemo.com")
