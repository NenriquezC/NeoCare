"""
TEST SUITE – Tarjetas (Cards)
Semana 2 – NeoCare Kanban

Este módulo contiene pruebas funcionales que verifican el comportamiento del
módulo "cards" (tarjetas). Las pruebas ejercitan la API completa a través del
cliente de pruebas de FastAPI (TestClient) y la base de datos real definida en
la configuración de pruebas.

Cobertura principal:
- Creación de tarjetas (válido / inválido)
- Validaciones de título y fecha (Pydantic)
- Edición de tarjetas
- Comprobación de acceso no autorizado y permisos entre usuarios
- Flujo completo: registro/login → crear → listar → editar

Notas importantes:
- Las pruebas usan el cliente TestClient y la sesión SQLAlchemy real (SessionLocal).
- Se generan correos aleatorios (con uuid) para evitar colisiones entre tests.
- Algunas pruebas manipulan la BD directamente para preparar estados (por ejemplo
crear un usuario A y una tarjeta privada) y luego utilizan la API para acciones
desde otro usuario B.
- Estas pruebas no requieren fixtures externas; sin embargo, se asume que la
configuración de la base de datos de pruebas y las migraciones están
preparadas antes de ejecutar la suite.
"""
from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal
from app.boards.models import User, Board, List, Card
import uuid


# Cliente global de pruebas (igual que sueles hacer en test_main.py)
client = TestClient(app)


# HELPERS 
def crear_usuario_y_token():
    """
    Registra un usuario vía API y devuelve el usuario persistido en BD y su token.

    Comportamiento:
    - Genera un email único con uuid para evitar colisiones entre pruebas.
    - Llama al endpoint /auth/register enviando email, password y name.
    - Verifica que la respuesta HTTP sea 200 y extrae access_token del JSON.
    - Recupera el usuario directamente desde la base de datos (SessionLocal).
    - Cierra la sesión y devuelve (user, token).

    Returns:
        tuple(User, str): instancia ORM del usuario y el token JWT (cadena).

    Raises / Asserts:
        - Aserta que la respuesta de registro es 200.
        - Aserta que el usuario existe en la BD tras el registro.
    """
    email = f"test_{uuid.uuid4().hex}@example.com"
    payload = {
        "email": email,
        "password": "password123",
        "name": "Tester",
    }

    resp = client.post("/auth/register", json=payload)
    assert resp.status_code == 200, resp.text
    data = resp.json()
    token = data["access_token"]

    # Recuperamos el usuario de la BD real
    db = SessionLocal()
    user = db.query(User).filter(User.email == email).first()
    db.close()

    assert user is not None
    return user, token


def crear_board_y_lista(user):
    """
    Crea directamente en la base de datos un Board y una List asociados a `user`.

    Este helper no usa la API, sino que inserta registros via ORM para preparar
    el estado necesario en las pruebas.

    Args:
        user (User): instancia ORM del usuario propietario del board.

    Returns:
        tuple(Board, List): las instancias ORM del tablero y de la lista creada.

    Side effects:
        - Inserta y comitea registros en la base de datos.
        - Devuelve objetos ya refrescados (con id) listos para usar en tests.
    """
    db = SessionLocal()
    board = Board(name="Tablero de pruebas", user_id=user.id)
    db.add(board)
    db.commit()
    db.refresh(board)

    lista = List(
        name="Por hacer",
        board_id=board.id,
        position=1,
    )
    db.add(lista)
    db.commit()
    db.refresh(lista)

    db.close()
    return board, lista


def crear_tarjeta_via_api(board, lista, headers):
    """
    Crea una tarjeta llamando a POST /cards/ y devuelve el JSON de respuesta.

    Args:
        board (Board): instancia ORM del tablero donde crear la tarjeta.
        lista (List): instancia ORM de la lista donde colocar la tarjeta.
        headers (dict): cabeceras HTTP a enviar (por ejemplo Authorization).

    Returns:
        dict: JSON parseado devuelto por la API que representa la tarjeta creada.

    Asserts:
        - Aserta que la respuesta HTTP sea 200.
    """
    payload = {
        "title": "Tarea de prueba",
        "description": "Descripción opcional",
        "due_date": "2025-12-31",
        "board_id": board.id,
        "list_id": lista.id,
    }

    resp = client.post("/cards/", json=payload, headers=headers)
    assert resp.status_code == 200, resp.text
    return resp.json()


#TESTS CREACIÓN 

def test_crear_tarjeta_ok():
    """
    Caso feliz: un usuario registrado crea una tarjeta válida.

    Flujo:
    - Registrar usuario y obtener token.
    - Crear board/list directamente en BD.
    - Llamar a la API para crear la tarjeta.
    - Comprobar que los campos devueltos coinciden y que la tarjeta existe en BD.

    Aserciones clave:
    - status 200 en creación.
    - título, board_id y list_id correctos en la respuesta.
    - la tarjeta existe efectivamente en la base de datos.
    """
    user, token = crear_usuario_y_token()
    board, lista = crear_board_y_lista(user)
    headers = {"Authorization": f"Bearer {token}"}

    card_data = crear_tarjeta_via_api(board, lista, headers)

    assert card_data["title"] == "Tarea de prueba"
    assert card_data["board_id"] == board.id
    assert card_data["list_id"] == lista.id

    # Confirmar que está en la BD
    db = SessionLocal()
    card_in_db = db.query(Card).filter(Card.id == card_data["id"]).first()
    db.close()
    assert card_in_db is not None


def test_crear_tarjeta_titulo_vacio():
    """
    Validación: intentar crear una tarjeta con título vacío debe fallar.

    Verifica que Pydantic / validación del endpoint rechaza título vacío con 422.
    """
    user, token = crear_usuario_y_token()
    board, lista = crear_board_y_lista(user)
    headers = {"Authorization": f"Bearer {token}"}

    payload = {
        "title": "",  # título vacío
        "description": "Sin título",
        "due_date": "2025-12-31",
        "board_id": board.id,
        "list_id": lista.id,
    }

    resp = client.post("/cards/", json=payload, headers=headers)
    assert resp.status_code == 422  # error de validación


def test_crear_tarjeta_fecha_invalida():
    """
    Validación: intentar crear una tarjeta con una fecha inválida debe fallar.

    Se espera un 422 porque Pydantic no puede parsear la fecha proporcionada.
    """
    user, token = crear_usuario_y_token()
    board, lista = crear_board_y_lista(user)
    headers = {"Authorization": f"Bearer {token}"}

    payload = {
        "title": "Fecha mala",
        "description": "Probando fecha inválida",
        "due_date": "2025-13-40",  # fecha imposible
        "board_id": board.id,
        "list_id": lista.id,
    }

    resp = client.post("/cards/", json=payload, headers=headers)
    assert resp.status_code == 422  # Pydantic no puede parsear la fecha


# TEST EDICIÓN

def test_editar_tarjeta_ok():
    """
    Edición de tarjeta: crear una tarjeta y luego editar sus campos (title, description).

    Flujo:
    - Registrar usuario y obtener token.
    - Preparar board/list y crear tarjeta vía API.
    - Llamar PATCH /cards/{id} con los campos a actualizar.
    - Verificar que la respuesta contiene los cambios y que la BD refleja los mismos.
    """
    user, token = crear_usuario_y_token()
    board, lista = crear_board_y_lista(user)
    headers = {"Authorization": f"Bearer {token}"}

    # Crear tarjeta
    card_data = crear_tarjeta_via_api(board, lista, headers)
    card_id = card_data["id"]

    # Editar
    update_payload = {
        "title": "Título editado",
        "description": "Descripción editada",
    }

    resp_update = client.patch(f"/cards/{card_id}", json=update_payload, headers=headers)
    assert resp_update.status_code == 200, resp_update.text

    data = resp_update.json()
    assert data["title"] == "Título editado"
    assert data["description"] == "Descripción editada"

    # Confirmar en BD
    db = SessionLocal()
    card_in_db = db.query(Card).filter(Card.id == card_id).first()
    db.close()
    assert card_in_db is not None
    assert card_in_db.title == "Título editado"
    assert card_in_db.description == "Descripción editada"


# TEST ERRORES Y PERMISOS 

def test_crear_tarjeta_sin_token():
    """
    Intento de creación sin autenticación: debe devolver 401 (no autorizado).

    No se envía cabecera Authorization y se espera que la API rechace la petición.
    """
    # No enviamos Authorization en headers
    payload = {
        "title": "Sin auth",
        "board_id": 1,
        "list_id": 1,
    }

    resp = client.post("/cards/", json=payload)
    assert resp.status_code == 401  # No autorizado


def test_ver_tarjeta_inexistente():
    """
    Petición GET a una tarjeta inexistente: se espera 404.
    """
    user, token = crear_usuario_y_token()
    headers = {"Authorization": f"Bearer {token}"}

    resp = client.get("/cards/999999", headers=headers)
    assert resp.status_code == 404


def test_no_puede_ver_tarjeta_de_otro_usuario():
    """
    Verificación de permisos entre usuarios:

    - Crea Usuario A en la BD y le crea un board/list y una tarjeta asociada.
    - Registra Usuario B vía API (para obtener token real).
    - Usuario B intenta acceder a la tarjeta de A y debe obtener 403 o 404
    (dependiendo de la implementación de permisos la API puede ocultar la
    existencia con 404 o devolver 403 por falta de permiso).
    """
    # Crear usuario A directamente en BD
    db = SessionLocal()
    user_a = User(
        email=f"a_{uuid.uuid4().hex}@example.com",
        password_hash="hash",
        name="User A",
    )
    db.add(user_a)
    db.commit()
    db.refresh(user_a)

    board_a = Board(name="Board A", user_id=user_a.id)
    db.add(board_a)
    db.commit()
    db.refresh(board_a)

    lista_a = List(name="Lista A", board_id=board_a.id, position=1)
    db.add(lista_a)
    db.commit()
    db.refresh(lista_a)

    card = Card(
        title="Tarjeta privada A",
        board_id=board_a.id,
        list_id=lista_a.id,
        created_by_id=user_a.id,
    )
    db.add(card)
    db.commit()
    db.refresh(card)
    db.close()

    # Crear usuario B vía API para tener token real
    email_b = f"b_{uuid.uuid4().hex}@example.com"
    payload_b = {
        "email": email_b,
        "password": "password123",
        "name": "User B",
    }
    resp_reg = client.post("/auth/register", json=payload_b)
    assert resp_reg.status_code == 200, resp_reg.text
    token_b = resp_reg.json()["access_token"]
    headers_b = {"Authorization": f"Bearer {token_b}"}

    # B intenta ver tarjeta de A
    resp = client.get(f"/cards/{card.id}", headers=headers_b)

    assert resp.status_code in (403, 404)


# TEST FLUJO COMPLETO

def test_flujo_completo_tarjeta():
    """
    Flujo funcional completo para una tarjeta:

    1. Registro (login implícito) y obtención de token.
    2. Creación de board/list y tarjeta.
    3. Listado de tarjetas por board.
    4. Edición de la tarjeta.
    5. Verificación de los cambios a través de la API.

    Aserciones:
    - La tarjeta creada aparece en el listado filtrado por board_id.
    - La edición mediante PATCH refleja los cambios en la respuesta.
    """
    user, token = crear_usuario_y_token()
    board, lista = crear_board_y_lista(user)
    headers = {"Authorization": f"Bearer {token}"}

    # Crear
    card_data = crear_tarjeta_via_api(board, lista, headers)
    card_id = card_data["id"]

    # Listar por tablero
    resp_list = client.get(f"/cards/?board_id={board.id}", headers=headers)
    assert resp_list.status_code == 200
    cards = resp_list.json()
    ids = [c["id"] for c in cards]
    assert card_id in ids

    # Editar
    update_payload = {
        "title": "Flujo - editada",
    }
    resp_update = client.patch(
        f"/cards/{card_id}",
        json=update_payload,
        headers=headers,
    )
    assert resp_update.status_code == 200
    data = resp_update.json()
    assert data["title"] == "Flujo - editada"