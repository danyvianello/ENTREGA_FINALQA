"""
Pruebas de API contra JSONPlaceholder (GET, POST, DELETE y encadenamiento).
"""

import pytest
import requests

from utils.lector_datos import leer_json
from utils.logger import log

API = leer_json("api.json")
URL_BASE = API["url_base"]
TIMEOUT = 15


@pytest.mark.api
def test_get_publicacion_existente():
    """GET /posts/1 debe devolver 200 y un JSON con id, title, body y userId."""
    respuesta = requests.get(f"{URL_BASE}/posts/1", timeout=TIMEOUT)
    log.info("GET /posts/1 -> %s", respuesta.status_code)

    assert respuesta.status_code == 200
    cuerpo = respuesta.json()
    assert cuerpo["id"] == 1
    assert "title" in cuerpo and cuerpo["title"]
    assert "body" in cuerpo and cuerpo["body"]
    assert cuerpo["userId"] == 1


@pytest.mark.api
@pytest.mark.negativo
def test_get_publicacion_inexistente():
    """GET de un id que no existe debe responder 404."""
    respuesta = requests.get(f"{URL_BASE}/posts/999999", timeout=TIMEOUT)
    log.info("GET /posts/999999 -> %s", respuesta.status_code)
    assert respuesta.status_code == 404


@pytest.mark.api
def test_post_crear_publicacion():
    """POST /posts crea un recurso y responde 201 con los campos enviados."""
    payload = API["post_nuevo"]
    respuesta = requests.post(f"{URL_BASE}/posts", json=payload, timeout=TIMEOUT)
    log.info("POST /posts -> %s", respuesta.status_code)

    assert respuesta.status_code == 201
    cuerpo = respuesta.json()
    assert cuerpo["title"] == payload["title"]
    assert cuerpo["body"] == payload["body"]
    assert cuerpo["userId"] == payload["userId"]
    assert "id" in cuerpo


@pytest.mark.api
def test_delete_publicacion():
    """DELETE /posts/1 debe responder 200."""
    respuesta = requests.delete(f"{URL_BASE}/posts/1", timeout=TIMEOUT)
    log.info("DELETE /posts/1 -> %s", respuesta.status_code)
    assert respuesta.status_code == 200


@pytest.mark.api
def test_encadenar_usuario_y_sus_posts():
    """GET usuario 1 y luego GET posts de ese userId (flujo dependiente)."""
    usuario = requests.get(f"{URL_BASE}/users/1", timeout=TIMEOUT)
    assert usuario.status_code == 200
    user_id = usuario.json()["id"]
    log.info("Usuario obtenido id=%s", user_id)

    posts = requests.get(f"{URL_BASE}/posts", params={"userId": user_id}, timeout=TIMEOUT)
    assert posts.status_code == 200
    lista = posts.json()
    assert isinstance(lista, list) and len(lista) > 0
    assert all(item["userId"] == user_id for item in lista)
    log.info("Posts del usuario %s: %s", user_id, len(lista))
