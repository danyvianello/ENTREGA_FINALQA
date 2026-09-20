# ENTREGA_FINALQA

# Proyecto Final: Framework de Automatización QA

Framework de pruebas automatizadas (UI + API) para la entrega final del curso.
Combina **Python**, **Pytest**, **Selenium WebDriver** (Page Object Model) y **Requests**,
con reportes HTML, logging, capturas ante fallos y un workflow opcional de GitHub Actions.

Sitio de UI: [saucedemo.com](https://www.saucedemo.com)  
API: [JSONPlaceholder](https://jsonplaceholder.typicode.com)

## Propósito

Demostrar un framework mantenible que:

- Automatiza flujos de UI (login, catálogo, carrito, checkout, logout y un caso negativo).
- Consume una API pública con GET, POST y DELETE, más un flujo encadenado.
- Separa tests de la interacción con la página (Page Object Model).
- Lee datos desde CSV/JSON y genera reportes claros.

## Tecnologías

| Pieza | Uso |
| --- | --- |
| Python 3.12 | Lenguaje |
| Pytest | Runner de tests |
| Selenium WebDriver | UI |
| Requests | API |
| pytest-html | Reporte HTML |
| Git / GitHub | Versiones y CI |

## Estructura

```
proyecto-final-automation-testing-marcos-vianello/
├── pages/                 # Page Object Model
│   ├── base_page.py
│   ├── login_page.py
│   ├── inventory_page.py
│   ├── cart_page.py
│   └── checkout_page.py
├── tests/
│   ├── ui/test_saucedemo.py
│   └── api/test_jsonplaceholder.py
├── utils/                 # driver, datos, logging
├── datos/                 # CSV / JSON de prueba
├── reports/               # HTML, capturas y logs
├── conftest.py
├── pytest.ini
└── .github/workflows/ci.yml
```

## Cómo instalar las dependencias

Requisitos: Python 3.10+ y Google Chrome.

```bash
cd proyecto-final-automation-testing-marcos-vianello
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Si `python3 -m venv` falla por falta de `ensurepip` en Ubuntu:

```bash
python3 -m venv --without-pip .venv
curl -sS https://bootstrap.pypa.io/get-pip.py -o /tmp/get-pip.py
.venv/bin/python3 /tmp/get-pip.py
.venv/bin/pip install -r requirements.txt
```

## Cómo ejecutar las pruebas

Desde la raíz, con el entorno activado:

```bash
pytest -v --html=reports/reporte.html --self-contained-html
```

Solo UI, solo API, o solo negativos:

```bash
pytest -m ui
pytest -m api
pytest -m negativo
```

Sin ventana (CI / servidor):

```bash
HEADLESS=1 pytest -v --html=reports/reporte.html --self-contained-html
```

## Cómo interpretar los reportes

1. Abrí `reports/reporte.html` en el navegador.
2. Cada fila es un test: estado (passed/failed), duración y detalle.
3. Si un test de UI falla, se adjunta una captura PNG y se guarda en `reports/capturas/` con fecha/hora y nombre del test.
4. Los pasos quedan en `reports/logs/ejecucion_AAAAMMDD.log`.

## Casos cubiertos

**UI (Sauce Demo)**

- Login exitoso (datos desde `datos/login.csv`).
- Login negativo: usuario bloqueado y credenciales inválidas.
- Catálogo: título, productos, menú y filtro.
- Alta al carrito parametrizada (`datos/productos.csv`).
- Checkout completo (`datos/checkout.json`).
- Logout.

**API (JSONPlaceholder)**

- GET de un post existente (200 + JSON).
- GET de un post inexistente (404).
- POST de un recurso (201).
- DELETE (200).
- Encadenamiento: usuario 1 → posts de ese `userId`.

Los tests son independientes: cada UI abre su propio navegador.

## CI/CD (opcional)

Al hacer push a `main`/`master`, GitHub Actions ejecuta `pytest` en headless y sube `reports/` como artefacto.
