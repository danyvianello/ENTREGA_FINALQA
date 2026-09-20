"""Página del carrito de compras."""

from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class CartPage(BasePage):
    ITEMS = (By.CSS_SELECTOR, ".cart_item, [data-test='inventory-item']")
    NOMBRE_ITEM = (By.CSS_SELECTOR, ".inventory_item_name, [data-test='inventory-item-name']")
    BOTON_CHECKOUT = (By.CSS_SELECTOR, "#checkout, [data-test='checkout']")

    def nombres_de_items(self) -> list[str]:
        self.encontrar_visible(self.NOMBRE_ITEM)
        return [el.text.strip() for el in self.driver.find_elements(*self.NOMBRE_ITEM)]

    def iniciar_checkout(self) -> None:
        self.clic(self.BOTON_CHECKOUT)
        self.wait.until(
            lambda driver: "checkout" in driver.current_url
            or bool(driver.find_elements(By.CSS_SELECTOR, "#first-name, [data-test='firstName']"))
        )
