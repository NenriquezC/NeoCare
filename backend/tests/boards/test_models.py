
"""
Pruebas unitarias para los modelos de la aplicación usando una base de datos SQLite en memoria.

Este módulo crea una base de datos en memoria (sqlite:///:memory:) y utiliza SQLAlchemy
para montar las tablas definidas en app.database.Base. Cada prueba utiliza la fixture
setup_db que crea las tablas antes de las pruebas y las destruye al finalizar.

Modelos probados:
- User
- Board
- List
- Card
- TimeEntry
- BoardMember

Notas:
- Las pruebas operan sobre objetos reales de los modelos y realizan commit/refresh
para verificar el comportamiento ORM (ids auto-generados, relaciones, valores de campos).
- La fixture setup_db tiene scope="module" para crear/derribar la BD una vez por módulo.
"""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base
from app.boards.models import User, Board, List, Card, TimeEntry, BoardMember
from datetime import date

# -------------------------
# Configurar DB en memoria
# -------------------------
engine = create_engine("sqlite:///:memory:", echo=False)
TestingSessionLocal = sessionmaker(bind=engine)

@pytest.fixture(scope="module")
def setup_db():
    """Fixture que prepara una base de datos SQLite en memoria para las pruebas.

    Crea todas las tablas definidas en Base.metadata antes de ceder la sesión de prueba,
    proporciona una sesión de SQLAlchemy (TestingSessionLocal) a las pruebas y realiza
    el teardown al cerrar la sesión y eliminar las tablas al final del módulo.

    Returns:
        Session: sesión de SQLAlchemy ligada a la base de datos de prueba.
    """
    # Crear tablas
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)

# -------------------------
# Tests User
# -------------------------
def test_create_user(setup_db):
    """Comprueba que se puede crear y persistir un User en la base de datos de prueba.

    Flujo:
    1. Crear una instancia User y añadirla a la sesión.
    2. Commit y refresh para obtener campos generados (p.ej. id).
    Aserciones:
    - user.id se ha generado (no es None).
    - user.email y user.name coinciden con los valores proporcionados.
    """
    db = setup_db
    user = User(email="test@example.com", password_hash="hashed_pw", name="Test User")
    db.add(user)
    db.commit()
    db.refresh(user)

    assert user.id is not None
    assert user.email == "test@example.com"
    assert user.name == "Test User"

# -------------------------
# Tests Board
# -------------------------
def test_create_board(setup_db):
    """Verifica la creación de un Board asociado a un User (owner).

    Flujo:
    1. Crear y persistir un User.
    2. Crear un Board asignándole owner y user_id.
    3. Commit y refresh del Board.
    Aserciones:
    - board.id se ha generado.
    - board.owner referencia al usuario creado.
    - board.name coincide con el valor esperado.
    """
    db = setup_db
    user = User(email="owner@example.com", password_hash="pw")
    db.add(user)
    db.commit()
    db.refresh(user)

    board = Board(name="Proyecto 1", owner=user, user_id=user.id)
    db.add(board)
    db.commit()
    db.refresh(board)

    assert board.id is not None
    assert board.owner == user
    assert board.name == "Proyecto 1"

# -------------------------
# Tests List
# -------------------------
def test_create_list(setup_db):
    """Verifica la creación de una List (lista de tareas) asociada a un Board.

    Flujo:
    1. Crear y persistir un User.
    2. Crear y persistir un Board asociado al usuario.
    3. Crear una List vinculada al Board y comprobar sus atributos.
    Aserciones:
    - list_.id se ha generado.
    - list_.board referencia al board creado.
    - list_.position coincide con el valor proporcionado.
    """
    db = setup_db
    user = User(email="listowner@example.com", password_hash="pw")
    db.add(user)
    db.commit()
    db.refresh(user)

    board = Board(name="Board List", owner=user, user_id=user.id)
    db.add(board)
    db.commit()
    db.refresh(board)

    list_ = List(name="To Do", board=board, board_id=board.id, position=1)
    db.add(list_)
    db.commit()
    db.refresh(list_)

    assert list_.id is not None
    assert list_.board == board
    assert list_.position == 1

# -------------------------
# Tests Card
# -------------------------
def test_create_card(setup_db):
    """Comprueba la creación de una Card asociada a un Board, List y usuarios responsables.

    Flujo:
    1. Crear y persistir un User.
    2. Crear y persistir un Board y una List.
    3. Crear una Card vinculada al Board y a la List; asignar created_by y responsible.
    4. Commit y refresh del Card.
    Aserciones:
    - card.id se ha generado.
    - card.board y card.list referencian las entidades creadas.
    - card.created_by y card.responsible referencian el usuario creado.
    """
    db = setup_db
    user = User(email="carduser@example.com", password_hash="pw")
    db.add(user)
    db.commit()
    db.refresh(user)

    board = Board(name="Board Card", owner=user, user_id=user.id)
    db.add(board)
    db.commit()
    db.refresh(board)

    list_ = List(name="Doing", board=board, board_id=board.id, position=1)
    db.add(list_)
    db.commit()
    db.refresh(list_)

    card = Card(
        title="Tarea 1",
        board=board,
        list=list_,
        board_id=board.id,
        list_id=list_.id,
        created_by=user,
        created_by_id=user.id,
        responsible=user,
        responsible_id=user.id,
        position=1,
    )
    db.add(card)
    db.commit()
    db.refresh(card)

    assert card.id is not None
    assert card.board == board
    assert card.list == list_
    assert card.created_by == user
    assert card.responsible == user

# -------------------------
# Tests TimeEntry
# -------------------------
def test_create_time_entry(setup_db):
    """Verifica la creación de una entrada de tiempo (TimeEntry) vinculada a un Card y un User.

    Flujo:
    1. Crear y persistir un User, Board, List y Card.
    2. Crear un TimeEntry con fecha y horas y vincularlo al card y user.
    3. Commit y refresh del TimeEntry.
    Aserciones:
    - entry.id se ha generado.
    - entry.user y entry.card referencian las entidades creadas.
    - entry.hours coincide con el valor insertado.
    """
    db = setup_db
    user = User(email="timeuser@example.com", password_hash="pw")
    db.add(user)
    db.commit()
    db.refresh(user)

    board = Board(name="Board Time", owner=user, user_id=user.id)
    db.add(board)
    db.commit()
    db.refresh(board)

    list_ = List(name="List Time", board=board, board_id=board.id, position=1)
    db.add(list_)
    db.commit()
    db.refresh(list_)

    card = Card(
        title="Card Time",
        board=board,
        list=list_,
        board_id=board.id,
        list_id=list_.id,
        created_by=user,
        created_by_id=user.id,
        responsible=user,
        responsible_id=user.id,
        position=1,
    )
    db.add(card)
    db.commit()
    db.refresh(card)

    entry = TimeEntry(user=user, user_id=user.id, card=card, card_id=card.id, date=date.today(), hours=2.5)
    db.add(entry)
    db.commit()
    db.refresh(entry)

    assert entry.id is not None
    assert entry.user == user
    assert entry.card == card
    assert entry.hours == 2.5

# -------------------------
# Tests BoardMember
# -------------------------
def test_create_board_member(setup_db):
    """Comprueba la creación de un BoardMember (miembro de tablero) y su asociación.

    Flujo:
    1. Crear y persistir un User y un Board.
    2. Crear un BoardMember asociándolo al board y al user con un role.
    3. Commit y refresh del BoardMember.
    Aserciones:
    - member.id se ha generado.
    - member.board y member.user referencian las entidades creadas.
    - member.role es el esperado ("admin").
    """
    db = setup_db
    user = User(email="member@example.com", password_hash="pw")
    db.add(user)
    db.commit()
    db.refresh(user)

    board = Board(name="Board Member", owner=user, user_id=user.id)
    db.add(board)
    db.commit()
    db.refresh(board)

    member = BoardMember(board=board, board_id=board.id, user=user, user_id=user.id, role="admin")
    db.add(member)
    db.commit()
    db.refresh(member)

    assert member.id is not None
    assert member.board == board
    assert member.user == user
    assert member.role == "admin"
