"""
Tests para Labels y Subtasks - Semana 6
Compatibles con SQLite
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app
from tests.conftest import TestingSessionLocal


@pytest.fixture
def preparar_tarjeta(client):
    """
    Fixture que crea usuario, tablero, lista y tarjeta para tests
    """
    # Registrar usuario
    client.post("/auth/register", json={
        "email": "test@test.com",
        "password": "Test1234!",
        "name": "Test User"
    })
    
    # Login (usar JSON, no form data)
    login_response = client.post("/auth/login", json={
        "email": "test@test.com",
        "password": "Test1234!"
    })
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # Obtener tableros (crea automáticamente si no existe)
    boards_response = client.get("/boards/", headers=headers)
    boards = boards_response.json()
    board_id = boards[0]["id"]
    
    # Obtener listas del tablero
    lists_response = client.get(f"/boards/{board_id}/lists", headers=headers)
    lists = lists_response.json()
    list_id = lists[0]["id"]
    
    # Crear tarjeta
    card_response = client.post(
        "/cards/",
        json={
            "board_id": board_id,
            "list_id": list_id,
            "title": "Tarjeta Test",
            "description": "Descripción de prueba"
        },
        headers=headers
    )
    card_id = card_response.json()["id"]
    
    return {
        "token": token,
        "headers": headers,
        "board_id": board_id,
        "list_id": list_id,
        "card_id": card_id
    }


# =====================================================================================
# 🏷️ TESTS DE LABELS
# =====================================================================================

def test_create_label(client, preparar_tarjeta):
    """
    Test: Crear una etiqueta en una tarjeta
    Verifica que se crea correctamente con nombre y color
    """
    data = preparar_tarjeta
    
    response = client.post(
        f"/cards/{data['card_id']}/labels",
        json={"name": "Urgente", "color": "#ef4444"},
        headers=data["headers"]
    )
    
    assert response.status_code == 200
    label = response.json()
    assert label["name"] == "Urgente"
    assert label["color"] == "#ef4444"
    assert label["card_id"] == data["card_id"]
    assert "id" in label


def test_get_card_labels(client, preparar_tarjeta):
    """
    Test: Obtener todas las etiquetas de una tarjeta
    """
    data = preparar_tarjeta
    
    # Crear 2 labels
    client.post(
        f"/cards/{data['card_id']}/labels",
        json={"name": "Urgente", "color": "#ef4444"},
        headers=data["headers"]
    )
    client.post(
        f"/cards/{data['card_id']}/labels",
        json={"name": "Feature", "color": "#3b82f6"},
        headers=data["headers"]
    )
    
    # Obtener labels
    response = client.get(
        f"/cards/{data['card_id']}/labels",
        headers=data["headers"]
    )
    
    assert response.status_code == 200
    labels = response.json()
    assert len(labels) == 2
    assert labels[0]["name"] == "Urgente"
    assert labels[1]["name"] == "Feature"


def test_delete_label(client, preparar_tarjeta):
    """
    Test: Eliminar una etiqueta
    """
    data = preparar_tarjeta
    
    # Crear label
    create_response = client.post(
        f"/cards/{data['card_id']}/labels",
        json={"name": "Temporal", "color": "#6b7280"},
        headers=data["headers"]
    )
    label_id = create_response.json()["id"]
    
    # Eliminar label
    delete_response = client.delete(
        f"/cards/labels/{label_id}",
        headers=data["headers"]
    )
    
    assert delete_response.status_code == 204
    
    # Verificar que no existe
    get_response = client.get(
        f"/cards/{data['card_id']}/labels",
        headers=data["headers"]
    )
    assert len(get_response.json()) == 0


def test_label_without_auth(client, preparar_tarjeta):
    """
    Test: Intentar crear label sin autenticación
    Debe retornar 401 Unauthorized
    """
    data = preparar_tarjeta
    
    response = client.post(
        f"/cards/{data['card_id']}/labels",
        json={"name": "Test", "color": "#000000"}
    )
    
    assert response.status_code == 401


# =====================================================================================
# ✅ TESTS DE SUBTASKS
# =====================================================================================

def test_create_subtask(client, preparar_tarjeta):
    """
    Test: Crear una subtarea en una tarjeta
    """
    data = preparar_tarjeta
    
    response = client.post(
        f"/cards/{data['card_id']}/subtasks",
        json={"title": "Escribir documentación", "completed": False},
        headers=data["headers"]
    )
    
    assert response.status_code == 200
    subtask = response.json()
    assert subtask["title"] == "Escribir documentación"
    assert subtask["completed"] == False
    assert subtask["card_id"] == data["card_id"]
    assert subtask["position"] == 0  # Primera subtask


def test_get_card_subtasks(client, preparar_tarjeta):
    """
    Test: Obtener todas las subtareas de una tarjeta
    Verifica que se ordenan por position
    """
    data = preparar_tarjeta
    
    # Crear 3 subtasks
    client.post(
        f"/cards/{data['card_id']}/subtasks",
        json={"title": "Primera tarea"},
        headers=data["headers"]
    )
    client.post(
        f"/cards/{data['card_id']}/subtasks",
        json={"title": "Segunda tarea"},
        headers=data["headers"]
    )
    client.post(
        f"/cards/{data['card_id']}/subtasks",
        json={"title": "Tercera tarea"},
        headers=data["headers"]
    )
    
    # Obtener subtasks
    response = client.get(
        f"/cards/{data['card_id']}/subtasks",
        headers=data["headers"]
    )
    
    assert response.status_code == 200
    subtasks = response.json()
    assert len(subtasks) == 3
    assert subtasks[0]["title"] == "Primera tarea"
    assert subtasks[0]["position"] == 0
    assert subtasks[2]["title"] == "Tercera tarea"
    assert subtasks[2]["position"] == 2


def test_update_subtask_completed(client, preparar_tarjeta):
    """
    Test: Marcar una subtarea como completada
    """
    data = preparar_tarjeta
    
    # Crear subtask
    create_response = client.post(
        f"/cards/{data['card_id']}/subtasks",
        json={"title": "Tarea para completar", "completed": False},
        headers=data["headers"]
    )
    subtask_id = create_response.json()["id"]
    
    # Marcar como completada
    update_response = client.patch(
        f"/cards/subtasks/{subtask_id}",
        json={"completed": True},
        headers=data["headers"]
    )
    
    assert update_response.status_code == 200
    updated = update_response.json()
    assert updated["completed"] == True
    assert updated["title"] == "Tarea para completar"  # No cambió


def test_update_subtask_title(client, preparar_tarjeta):
    """
    Test: Actualizar el título de una subtarea
    """
    data = preparar_tarjeta
    
    # Crear subtask
    create_response = client.post(
        f"/cards/{data['card_id']}/subtasks",
        json={"title": "Título original"},
        headers=data["headers"]
    )
    subtask_id = create_response.json()["id"]
    
    # Actualizar título
    update_response = client.patch(
        f"/cards/subtasks/{subtask_id}",
        json={"title": "Título actualizado"},
        headers=data["headers"]
    )
    
    assert update_response.status_code == 200
    updated = update_response.json()
    assert updated["title"] == "Título actualizado"


def test_delete_subtask(client, preparar_tarjeta):
    """
    Test: Eliminar una subtarea
    """
    data = preparar_tarjeta
    
    # Crear subtask
    create_response = client.post(
        f"/cards/{data['card_id']}/subtasks",
        json={"title": "Tarea temporal"},
        headers=data["headers"]
    )
    subtask_id = create_response.json()["id"]
    
    # Eliminar
    delete_response = client.delete(
        f"/cards/subtasks/{subtask_id}",
        headers=data["headers"]
    )
    
    assert delete_response.status_code == 204
    
    # Verificar que no existe
    get_response = client.get(
        f"/cards/{data['card_id']}/subtasks",
        headers=data["headers"]
    )
    assert len(get_response.json()) == 0


def test_subtask_progress_calculation(client, preparar_tarjeta):
    """
    Test: Simular cálculo de progreso de checklist
    Frontend debe poder calcular: completadas/total
    """
    data = preparar_tarjeta
    
    # Crear 5 subtasks
    subtask_ids = []
    for i in range(5):
        response = client.post(
            f"/cards/{data['card_id']}/subtasks",
            json={"title": f"Tarea {i+1}"},
            headers=data["headers"]
        )
        subtask_ids.append(response.json()["id"])
    
    # Completar 3 de 5
    for i in [0, 1, 2]:
        client.patch(
            f"/cards/subtasks/{subtask_ids[i]}",
            json={"completed": True},
            headers=data["headers"]
        )
    
    # Obtener y verificar
    response = client.get(
        f"/cards/{data['card_id']}/subtasks",
        headers=data["headers"]
    )
    subtasks = response.json()
    
    completed = sum(1 for st in subtasks if st["completed"])
    total = len(subtasks)
    percentage = (completed / total) * 100
    
    assert completed == 3
    assert total == 5
    assert percentage == 60.0


# =====================================================================================
# 🔍 TESTS DE BÚSQUEDA Y FILTRADO
# =====================================================================================

def test_search_cards_by_title(client, preparar_tarjeta):
    """
    Test: Buscar tarjetas por título
    """
    data = preparar_tarjeta
    
    # Crear varias tarjetas
    client.post(
        "/cards/",
        json={
            "board_id": data["board_id"],
            "list_id": data["list_id"],
            "title": "Implementar API de búsqueda",
            "description": "Backend"
        },
        headers=data["headers"]
    )
    client.post(
        "/cards/",
        json={
            "board_id": data["board_id"],
            "list_id": data["list_id"],
            "title": "Diseñar UI de login",
            "description": "Frontend"
        },
        headers=data["headers"]
    )
    
    # Buscar "API"
    response = client.get(
        f"/cards/?board_id={data['board_id']}&search=API",
        headers=data["headers"]
    )
    
    assert response.status_code == 200
    cards = response.json()
    assert len(cards) == 1
    assert "API" in cards[0]["title"]


def test_search_cards_by_description(client, preparar_tarjeta):
    """
    Test: Buscar tarjetas por descripción
    """
    data = preparar_tarjeta
    
    # Crear tarjeta con palabra en descripción
    client.post(
        "/cards/",
        json={
            "board_id": data["board_id"],
            "list_id": data["list_id"],
            "title": "Tarea sin keyword",
            "description": "Implementar autenticación JWT urgente"
        },
        headers=data["headers"]
    )
    
    # Buscar "JWT"
    response = client.get(
        f"/cards/?board_id={data['board_id']}&search=JWT",
        headers=data["headers"]
    )
    
    assert response.status_code == 200
    cards = response.json()
    assert len(cards) >= 1
    assert any("JWT" in card["description"] for card in cards)


def test_filter_by_responsible(client, preparar_tarjeta):
    """
    Test: Filtrar tarjetas por responsable
    Nota: Requiere endpoint de usuarios o usar el usuario actual
    """
    data = preparar_tarjeta
    
    # Este test es básico - idealmente necesitarías crear varios usuarios
    # Por ahora solo verificamos que el parámetro no rompe nada
    response = client.get(
        f"/cards/?board_id={data['board_id']}&responsible_id=1",
        headers=data["headers"]
    )
    
    assert response.status_code == 200
    # El filtro debería funcionar (aunque no haya cards con ese responsable)


def test_combined_filters(client, preparar_tarjeta):
    """
    Test: Combinar búsqueda + filtro de lista
    """
    data = preparar_tarjeta
    
    # Crear tarjetas en diferentes contextos
    client.post(
        "/cards/",
        json={
            "board_id": data["board_id"],
            "list_id": data["list_id"],
            "title": "Bug urgente en producción",
        },
        headers=data["headers"]
    )
    
    # Buscar "urgente" en lista específica
    response = client.get(
        f"/cards/?board_id={data['board_id']}&search=urgente&list_id={data['list_id']}",
        headers=data["headers"]
    )
    
    assert response.status_code == 200
    cards = response.json()
    assert all(card["list_id"] == data["list_id"] for card in cards)
