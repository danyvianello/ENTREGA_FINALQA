"""
Casos de UI sobre saucedemo.com (Page Object Model).

Flujos: login, catálogo, carrito, checkout y un escenario negativo.
Los datos salen de datos/login.csv, datos/productos.csv y datos/checkout.json.
"""

import pytest

from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from utils.lector_datos import casos_login_por_escenario, leer_json, nombres_productos
from utils.logger import log

CASOS_VALIDOS = casos_login_por_escenario("valido")
CASOS_NEGATIVOS = [
    caso
    for caso in casos_login_por_escenario("bloqueado") + casos_login_por_escenario("invalido")
]


@pytest.mark.ui
@pytest.mark.parametrize(
    "usuario,contrasena",
    [(c["usuario"], c["contrasena"]) for c in CASOS_VALIDOS],
    ids=[c["usuario"] for c in CASOS_VALIDOS],
)
def test_login_exitoso(navegador, usuario, contrasena):
    """Login válido y redirección al inventario."""
    login = LoginPage(navegador)
    login.abrir()
    login.iniciar_sesion(usuario, contrasena)

    inventario = InventoryPage(navegador)
    inventario.url_contiene("/inventory.html")

    assert "/inventory.html" in navegador.current_url
    assert inventario.titulo_visible() == "Products"
    assert "Swag Labs" in inventario.logo_visible()
    log.info("Login exitoso validado para %s", usuario)


@pytest.mark.ui
@pytest.mark.negativo
@pytest.mark.parametrize(
    "usuario,contrasena,mensaje_esperado",
    [(c["usuario"], c["contrasena"], c["mensaje_esperado"]) for c in CASOS_NEGATIVOS],
    ids=[c["escenario"] for c in CASOS_NEGATIVOS],
)
def test_login_credenciales_invalidas(navegador, usuario, contrasena, mensaje_esperado):
    """Login bloqueado o usuario inexistente: debe mostrarse el error esperado."""
    login = LoginPage(navegador)
    login.abrir()
    login.iniciar_sesion(usuario, contrasena)

    error = login.mensaje_de_error()
    assert mensaje_esperado in error, f"Mensaje inesperado: {error}"
    assert "/inventory.html" not in navegador.current_url
    log.info("Login negativo validado (%s)", usuario)


@pytest.mark.ui
def test_catalogo_muestra_productos_y_controles(sesion_logueada):
    """El inventario tiene título, productos, menú y filtro."""
    inventario = InventoryPage(sesion_logueada)
    assert inventario.titulo_visible() == "Products"
    assert inventario.cantidad_productos() >= 1
    inventario.menu_y_filtro_visibles()
    log.info("Catálogo verificado: %s productos", inventario.cantidad_productos())


@pytest.mark.ui
@pytest.mark.parametrize("nombre_producto", nombres_productos())
def test_agregar_producto_al_carrito(sesion_logueada, nombre_producto):
    """Agrega un producto parametrizado y lo verifica en el carrito."""
    inventario = InventoryPage(sesion_logueada)
    inventario.agregar_producto(nombre_producto)
    assert inventario.contador_carrito() == "1"

    inventario.ir_al_carrito()
    carrito = CartPage(sesion_logueada)
    assert nombre_producto in carrito.nombres_de_items()
    log.info("Producto en carrito: %s", nombre_producto)


@pytest.mark.ui
def test_checkout_completo(sesion_logueada):
    """Flujo completo: producto -> carrito -> datos -> compra finalizada."""
    datos = leer_json("checkout.json")
    producto = nombres_productos()[0]

    inventario = InventoryPage(sesion_logueada)
    inventario.agregar_producto(producto)
    inventario.ir_al_carrito()

    carrito = CartPage(sesion_logueada)
    carrito.iniciar_checkout()

    checkout = CheckoutPage(sesion_logueada)
    checkout.completar_datos(datos["nombre"], datos["apellido"], datos["codigo_postal"])
    checkout.finalizar()

    mensaje = checkout.mensaje_compra_exitosa()
    assert "Thank you for your order" in mensaje
    log.info("Checkout completado: %s", mensaje)


@pytest.mark.ui
def test_logout_vuelve_al_login(sesion_logueada):
    """Cerrar sesión desde el menú y volver al formulario de login."""
    inventario = InventoryPage(sesion_logueada)
    inventario.cerrar_sesion()
    login = LoginPage(sesion_logueada)
    login.encontrar_visible(login.CAMPO_USUARIO)
    assert "inventory" not in sesion_logueada.current_url
    log.info("Logout verificado")
