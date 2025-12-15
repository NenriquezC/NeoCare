import os
import time
import uuid

import pytest
import requests


# Configuración de URLs (se pueden sobrescribir por variables de entorno)
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")
BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")


def _ensure_user(email: str, password: str, name: str = "E2E User"):
    """Crea un usuario de prueba vía API; si ya existe, el error 400 se ignora.

    Se basa en el endpoint real /auth/register, que también crea el tablero y las
    listas por defecto ("Por hacer", "En curso", "Hecho").
    """

    payload = {"email": email, "password": password, "name": name}
    res = requests.post(f"{BACKEND_URL}/auth/register", json=payload, timeout=10)

    if res.status_code == 200:
        return

    if res.status_code == 400 and "Email ya registrado" in res.text:
        # El usuario ya existe; seguimos adelante para usarlo en las pruebas.
        return

    raise RuntimeError(f"No se pudo preparar el usuario de pruebas: {res.status_code} {res.text}")


@pytest.fixture(scope="session")
def test_user():
    """Genera un usuario único para toda la sesión de pruebas E2E."""

    unique = uuid.uuid4().hex[:8]
    email = f"e2e_{unique}@example.com"
    password = "Password123!"
    _ensure_user(email, password)
    return {"email": email, "password": password}


def ui_login(page, email: str, password: str):
    """Realiza login vía UI y espera la carga de /boards."""

    page.goto(f"{FRONTEND_URL}/login")
    page.fill("input[type=email]", email)
    page.fill("input[type=password]", password)
    page.click("button[type=submit]")
    page.wait_for_url("**/boards")


def test_login_exitoso_muestra_tablero(page, test_user):
    """Login correcto y render de columnas principales."""

    ui_login(page, test_user["email"], test_user["password"])
    page.wait_for_selector("text=Por hacer")
    page.wait_for_selector("text=En curso")
    page.wait_for_selector("text=Hecho")


def test_login_fallido_muestra_error(page):
    """Login con credenciales inválidas muestra mensaje de error."""

    page.goto(f"{FRONTEND_URL}/login")
    page.fill("input[type=email]", "wrong@example.com")
    page.fill("input[type=password]", "badpass")
    page.click("button[type=submit]")
    page.wait_for_selector("text=No se ha podido iniciar sesión")


def test_crud_tarjeta_en_primer_tablero(page, test_user):
    """Crea, edita y elimina una tarjeta usando la UI del tablero."""

    ui_login(page, test_user["email"], test_user["password"])

    # Esperar a que las columnas estén listas
    page.wait_for_selector("text=Por hacer")

    # Crear tarjeta
    title = f"Tarea {int(time.time() * 1000)}"
    desc = "Descripción E2E"
    new_title = f"{title} editada"

    page.get_by_text("+ Nueva tarjeta").click()
    form = page.locator("form")
    form.locator("input").first.fill(title)
    form.locator("textarea").first.fill(desc)
    form.locator("button", has_text="Crear tarjeta").click()
    page.wait_for_selector(f"text={title}")

    # Editar tarjeta (click en la tarjeta para abrir modal)
    page.get_by_text(title).click()
    form.locator("input").first.fill(new_title)
    form.locator("button", has_text="Guardar cambios").click()
    page.wait_for_selector(f"text={new_title}")

    # Eliminar tarjeta (aceptar diálogo de confirmación)
    page.get_by_text(new_title).click()
    page.once("dialog", lambda dialog: dialog.accept())
    form.locator("button", has_text="Eliminar").click()
    page.wait_for_timeout(300)  # pequeño margen para que desaparezca
    assert page.query_selector(f"text={new_title}") is None
