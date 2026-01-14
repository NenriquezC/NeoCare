import os
import time
import uuid
from datetime import date

import pytest
import requests


# Configuración de URLs
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")
BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")


def _ensure_user(email: str, password: str, name: str = "E2E User"):
    """Crea un usuario de prueba vía API."""
    payload = {"email": email, "password": password, "name": name}
    res = requests.post(f"{BACKEND_URL}/auth/register", json=payload, timeout=10)
    
    if res.status_code in [200, 201]:
        return res.json().get("access_token")
    
    if res.status_code == 400 and "Email ya registrado" in res.text:
        # Login si ya existe
        login_res = requests.post(f"{BACKEND_URL}/auth/login", json={"email": email, "password": password}, timeout=10)
        return login_res.json().get("access_token")
    
    raise RuntimeError(f"No se pudo preparar el usuario: {res.status_code} {res.text}")


@pytest.fixture(scope="session")
def test_user():
    """Genera un usuario único para toda la sesión."""
    unique = uuid.uuid4().hex[:8]
    email = f"e2e_{unique}@example.com"
    password = "Password123!"
    token = _ensure_user(email, password)
    return {"email": email, "password": password, "token": token}


# ========================
# TESTS DE BOARDS (GET)
# ========================

def test_api_get_boards(test_user):
    """GET /boards/ - Obtiene los tableros del usuario"""
    headers = {"Authorization": f"Bearer {test_user['token']}"}
    res = requests.get(f"{BACKEND_URL}/boards/", headers=headers, timeout=10)
    
    assert res.status_code == 200, f"Error al obtener boards: {res.text}"
    boards = res.json()
    assert isinstance(boards, list), "La respuesta debe ser una lista"
    assert len(boards) > 0, "Debe haber al menos 1 board"
    
    # Guardar board_id para usar en otros tests
    test_user["board_id"] = boards[0]["id"]
    print(f"✅ Board obtenido: ID={boards[0]['id']}, Nombre={boards[0]['name']}")


# ========================
# TESTS DE LISTS (GET)
# ========================

def test_api_get_lists(test_user):
    """GET /boards/{board_id}/lists/ - Obtiene las listas del tablero"""
    board_id = test_user.get("board_id", 1)  # Usar el board del test anterior
    headers = {"Authorization": f"Bearer {test_user['token']}"}
    res = requests.get(f"{BACKEND_URL}/boards/{board_id}/lists/", headers=headers, timeout=10)
    
    assert res.status_code == 200, f"Error al obtener lists: {res.text}"
    lists = res.json()
    assert isinstance(lists, list), "La respuesta debe ser una lista"
    assert len(lists) >= 3, "Debe haber al menos 3 listas (Por hacer, En curso, Hecho)"
    
    # Guardar list_id para tests de cards
    test_user["list_id"] = lists[0]["id"]
    print(f"✅ Lists obtenidas: {len(lists)} listas")


# ========================
# TESTS DE CARDS (CRUD COMPLETO)
# ========================

def test_api_create_card(test_user):
    """POST /cards/ - Crear una nueva tarjeta"""
    board_id = test_user.get("board_id", 1)
    list_id = test_user.get("list_id", 1)
    headers = {"Authorization": f"Bearer {test_user['token']}"}
    
    payload = {
        "title": f"Tarjeta E2E {int(time.time())}",
        "description": "Descripción de prueba E2E",
        "due_date": "2025-12-31",
        "board_id": board_id,
        "list_id": list_id
    }
    
    res = requests.post(f"{BACKEND_URL}/cards/", json=payload, headers=headers, timeout=10)
    assert res.status_code == 200, f"Error al crear card: {res.text}"
    
    card = res.json()
    assert "id" in card, "La respuesta debe contener el ID de la tarjeta"
    assert card["title"] == payload["title"], "El título debe coincidir"
    
    test_user["card_id"] = card["id"]
    print(f"✅ Card creada: ID={card['id']}, Título={card['title']}")


def test_api_list_cards(test_user):
    """GET /cards/?board_id={board_id} - Listar tarjetas del tablero"""
    board_id = test_user.get("board_id", 1)
    headers = {"Authorization": f"Bearer {test_user['token']}"}
    
    res = requests.get(f"{BACKEND_URL}/cards/?board_id={board_id}", headers=headers, timeout=10)
    assert res.status_code == 200, f"Error al listar cards: {res.text}"
    
    cards = res.json()
    assert isinstance(cards, list), "La respuesta debe ser una lista"
    assert len(cards) > 0, "Debe haber al menos 1 tarjeta"
    print(f"✅ Cards listadas: {len(cards)} tarjetas")


def test_api_get_card_detail(test_user):
    """GET /cards/{card_id} - Obtener detalle de una tarjeta"""
    card_id = test_user.get("card_id")
    headers = {"Authorization": f"Bearer {test_user['token']}"}
    
    res = requests.get(f"{BACKEND_URL}/cards/{card_id}", headers=headers, timeout=10)
    assert res.status_code == 200, f"Error al obtener card: {res.text}"
    
    card = res.json()
    assert card["id"] == card_id, "El ID debe coincidir"
    print(f"✅ Card detalle obtenida: {card['title']}")


def test_api_update_card_patch(test_user):
    """PATCH /cards/{card_id} - Actualizar parcialmente una tarjeta"""
    card_id = test_user.get("card_id")
    headers = {"Authorization": f"Bearer {test_user['token']}"}
    
    payload = {"title": "Tarjeta Actualizada PATCH"}
    res = requests.patch(f"{BACKEND_URL}/cards/{card_id}", json=payload, headers=headers, timeout=10)
    
    assert res.status_code == 200, f"Error al actualizar card (PATCH): {res.text}"
    card = res.json()
    assert card["title"] == payload["title"], "El título debe estar actualizado"
    print(f"✅ Card actualizada (PATCH): {card['title']}")


def test_api_update_card_put(test_user):
    """PUT /cards/{card_id} - Actualizar completamente una tarjeta"""
    card_id = test_user.get("card_id")
    board_id = test_user.get("board_id", 1)
    list_id = test_user.get("list_id", 1)
    headers = {"Authorization": f"Bearer {test_user['token']}"}
    
    payload = {
        "title": "Tarjeta Actualizada PUT",
        "description": "Nueva descripción completa",
        "due_date": "2025-12-25",
        "board_id": board_id,
        "list_id": list_id
    }
    
    res = requests.put(f"{BACKEND_URL}/cards/{card_id}", json=payload, headers=headers, timeout=10)
    assert res.status_code == 200, f"Error al actualizar card (PUT): {res.text}"
    
    card = res.json()
    assert card["title"] == payload["title"], "El título debe estar actualizado"
    print(f"✅ Card actualizada (PUT): {card['title']}")


def test_api_move_card(test_user):
    """PATCH /cards/{card_id}/move - Mover tarjeta a otra posición"""
    card_id = test_user.get("card_id")
    list_id = test_user.get("list_id", 1)
    headers = {"Authorization": f"Bearer {test_user['token']}"}
    
    payload = {"list_id": list_id, "order": 0}
    res = requests.patch(f"{BACKEND_URL}/cards/{card_id}/move", json=payload, headers=headers, timeout=10)
    
    assert res.status_code == 200, f"Error al mover card: {res.text}"
    print(f"✅ Card movida correctamente")


def test_api_delete_card(test_user):
    """DELETE /cards/{card_id} - Eliminar una tarjeta"""
    card_id = test_user.get("card_id")
    headers = {"Authorization": f"Bearer {test_user['token']}"}
    
    res = requests.delete(f"{BACKEND_URL}/cards/{card_id}", headers=headers, timeout=10)
    assert res.status_code == 204, f"Error al eliminar card: {res.text}"
    
    # Verificar que ya no existe
    get_res = requests.get(f"{BACKEND_URL}/cards/{card_id}", headers=headers, timeout=10)
    assert get_res.status_code == 404, "La tarjeta debería estar eliminada"
    print(f"✅ Card eliminada correctamente")


# ========================
# TESTS DE WORKLOGS (API)
# ========================

def test_api_create_worklog(test_user):
    """POST /worklogs/ - Registrar horas en una tarjeta"""
    # Necesitamos una tarjeta para registrar horas
    headers = {"Authorization": f"Bearer {test_user['token']}"}
    
    # 1. Obtener el tablero por defecto (el backend lo crea automáticamente al hacer GET /boards/)
    boards_res = requests.get(f"{BACKEND_URL}/boards/", headers=headers)
    boards = boards_res.json()
    assert len(boards) > 0, "No se encontraron tableros"
    board_id = boards[0]["id"]
    
    # 2. Obtener las listas del tablero
    lists_res = requests.get(f"{BACKEND_URL}/boards/{board_id}/lists/", headers=headers)
    lists = lists_res.json()
    assert len(lists) > 0, "No se encontraron listas"
    list_id = lists[0]["id"]

    # 3. Crear una tarjeta temporal
    card_payload = {
        "title": "Tarjeta para Worklog E2E",
        "board_id": board_id,
        "list_id": list_id
    }
    card_res = requests.post(f"{BACKEND_URL}/cards/", json=card_payload, headers=headers)
    assert card_res.status_code == 200, f"Error al crear tarjeta: {card_res.text}"
    card_id = card_res.json()["id"]
    
    # 4. Registrar horas
    worklog_payload = {
        "card_id": card_id,
        "date": date.today().isoformat(),
        "hours": 4.5,
        "note": "Registro E2E"
    }
    res = requests.post(f"{BACKEND_URL}/worklogs/", json=worklog_payload, headers=headers)
    
    # Si falla con 403, imprimimos el detalle para depurar
    if res.status_code != 201:
        print(f"DEBUG: Error 403 en worklog. UserID del token: {test_user['email']}")
        print(f"DEBUG: CardID: {card_id}, BoardID: {board_id}")
        print(f"DEBUG: Response: {res.text}")
        
    assert res.status_code == 201
    print(f"✅ Worklog creado vía API: 4.5h")


# ========================
# TESTS UI (Playwright)
# ========================

def ui_login(page, email: str, password: str):
    """Realiza login vía UI"""
    page.goto(f"{FRONTEND_URL}/login")
    page.fill("input[type=email]", email)
    page.fill("input[type=password]", password)
    page.click("button[type=submit]")
    page.wait_for_url("**/boards")


def test_ui_login_exitoso(page, test_user):
    """Login correcto muestra el tablero"""
    ui_login(page, test_user["email"], test_user["password"])
    page.wait_for_selector("text=Por hacer")
    page.wait_for_selector("text=En curso")
    page.wait_for_selector("text=Hecho")
    print("✅ UI: Login exitoso y tablero cargado")


def test_ui_worklogs_page(page, test_user):
    """Navegar a Mis Horas y ver registros"""
    ui_login(page, test_user["email"], test_user["password"])
    
    # Click en el enlace de Mis Horas (ajustar selector según tu sidebar)
    page.click("text=Mis horas")
    page.wait_for_url("**/my-hours")
    
    # Verificar que aparece el título y al menos el registro que creamos por API
    page.wait_for_selector("text=Mis horas")
    page.wait_for_selector("text=4.50") # Las horas se formatean a 2 decimales
    print("✅ UI: Página de Mis Horas cargada con datos")


def test_ui_login_fallido(page):
    """Login con credenciales inválidas muestra error"""
    page.goto(f"{FRONTEND_URL}/login")
    page.fill("input[type=email]", "wrong@example.com")
    page.fill("input[type=password]", "badpass")
    page.click("button[type=submit]")
    # El frontend muestra "Error: " + el mensaje JSON del backend
    page.wait_for_selector("text=Error:", timeout=5000)
    print("✅ UI: Login fallido muestra error")


# ========================
# TEST E2E COMPLETO - WORKLOGS
# ========================

def test_e2e_worklogs_complete_flow(test_user):
    """
    Test E2E completo del flujo de worklogs:
    1. Crear tarjeta
    2. Añadir horas a la tarjeta
    3. Listar horas de la tarjeta
    4. Editar horas
    5. Ver horas en "Mis Horas" (semana actual)
    6. Eliminar horas
    7. Verificar eliminación
    """
    headers = {"Authorization": f"Bearer {test_user['token']}"}
    board_id = test_user.get("board_id", 1)
    list_id = test_user.get("list_id", 1)

    # 1. Crear tarjeta
    print("\n📝 Paso 1: Crear tarjeta para worklog...")
    card_payload = {
        "title": f"Tarjeta E2E Worklogs {int(time.time())}",
        "description": "Tarjeta para testing completo de worklogs",
        "board_id": board_id,
        "list_id": list_id
    }
    res_card = requests.post(f"{BACKEND_URL}/cards/", json=card_payload, headers=headers, timeout=10)
    assert res_card.status_code == 200, f"Error creando tarjeta: {res_card.text}"
    card = res_card.json()
    card_id = card["id"]
    print(f"✅ Tarjeta creada: ID={card_id}")

    # 2. Añadir horas (worklog)
    print("\n⏱️ Paso 2: Añadir registro de horas...")
    today = date.today()
    worklog_payload = {
        "card_id": card_id,
        "date": str(today),
        "hours": 3.5,
        "note": "Testing E2E worklogs"
    }
    res_create_worklog = requests.post(
        f"{BACKEND_URL}/worklogs/",
        json=worklog_payload,
        headers=headers,
        timeout=10
    )
    assert res_create_worklog.status_code == 201, f"Error creando worklog: {res_create_worklog.text}"
    worklog = res_create_worklog.json()
    worklog_id = worklog["id"]
    assert worklog["hours"] == "3.50"
    assert worklog["note"] == "Testing E2E worklogs"
    print(f"✅ Worklog creado: ID={worklog_id}, Horas={worklog['hours']}")

    # 3. Listar horas de la tarjeta
    print("\n📋 Paso 3: Listar worklogs de la tarjeta...")
    res_list = requests.get(
        f"{BACKEND_URL}/worklogs/card/{card_id}",
        headers=headers,
        timeout=10
    )
    assert res_list.status_code == 200, f"Error listando worklogs: {res_list.text}"
    worklogs = res_list.json()
    assert isinstance(worklogs, list)
    assert len(worklogs) >= 1
    found_worklog = next((w for w in worklogs if w["id"] == worklog_id), None)
    assert found_worklog is not None, "Worklog creado no encontrado en listado"
    print(f"✅ Worklogs listados: {len(worklogs)} registro(s)")

    # 4. Editar horas
    print("\n✏️ Paso 4: Editar registro de horas...")
    update_payload = {
        "hours": 5.0,
        "note": "Horas actualizadas en E2E"
    }
    res_update = requests.patch(
        f"{BACKEND_URL}/worklogs/{worklog_id}",
        json=update_payload,
        headers=headers,
        timeout=10
    )
    assert res_update.status_code == 200, f"Error actualizando worklog: {res_update.text}"
    updated_worklog = res_update.json()
    assert updated_worklog["hours"] == "5.00"
    assert updated_worklog["note"] == "Horas actualizadas en E2E"
    print(f"✅ Worklog actualizado: Horas={updated_worklog['hours']}")

    # 5. Ver en "Mis Horas" (semana actual)
    print("\n📊 Paso 5: Verificar en 'Mis Horas' (semana actual)...")
    year, week_num, _ = today.isocalendar()
    week_str = f"{year}-{week_num:02d}"
    res_my_hours = requests.get(
        f"{BACKEND_URL}/worklogs/me/week?week={week_str}",
        headers=headers,
        timeout=10
    )
    assert res_my_hours.status_code == 200, f"Error obteniendo mis horas: {res_my_hours.text}"
    my_hours = res_my_hours.json()
    assert my_hours["week"] == week_str
    assert float(my_hours["total_hours"]) >= 5.0
    assert len(my_hours["entries"]) >= 1
    print(f"✅ Mis horas verificadas: Semana={week_str}, Total={my_hours['total_hours']}h")

    # 6. Eliminar horas
    print("\n🗑️ Paso 6: Eliminar registro de horas...")
    res_delete = requests.delete(
        f"{BACKEND_URL}/worklogs/{worklog_id}",
        headers=headers,
        timeout=10
    )
    assert res_delete.status_code == 204, f"Error eliminando worklog: {res_delete.text}"
    print(f"✅ Worklog eliminado: ID={worklog_id}")

    # 7. Verificar eliminación
    print("\n🔍 Paso 7: Verificar eliminación...")
    res_verify = requests.get(
        f"{BACKEND_URL}/worklogs/card/{card_id}",
        headers=headers,
        timeout=10
    )
    assert res_verify.status_code == 200
    remaining_worklogs = res_verify.json()
    deleted_worklog = next((w for w in remaining_worklogs if w["id"] == worklog_id), None)
    assert deleted_worklog is None, "Worklog no fue eliminado correctamente"
    print("✅ Worklog eliminado correctamente")

    print("\n🎉 Flujo E2E de Worklogs completado exitosamente!")



