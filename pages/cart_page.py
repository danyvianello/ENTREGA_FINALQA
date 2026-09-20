"""Página del carrito de compras."""

from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class CartPage(BasePage):
    ITEMS = (By.CLASS_NAME, "cart_item")
    NOMBRE_ITEM = (By.CLASS_NAME, "inventory_item_name")
    BOTON_CHECKOUT = (By.ID, "checkout")

    def nombres_de_items(self) -> list[str]:
        self.encontrar_visible(self.ITEMS)
        return [el.text for el in self.driver.find_elements(*self.NOMBRE_ITEM)]

    def iniciar_checkout(self) -> None:
        self.clic(self.BOTON_CHECKOUT)
        self.url_contiene("checkout-step-one")
