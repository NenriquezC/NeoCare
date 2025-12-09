
"""
tests/test_models.py
--------------------

Pruebas unitarias para los modelos del dominio "boards" usando SQLAlchemy y
una base de datos SQLite en memoria. Estas pruebas verifican que las entidades
principales (User, Board, List, Card, TimeEntry, BoardMember) puedan ser
creadas, persistidas y relaciones básicas entre ellas funcionen correctamente.

Notas importantes sobre el enfoque:
- Se utiliza un engine SQLite en memoria para aislamiento y velocidad.
- El fixture `setup_db` tiene alcance "module": crea las tablas al inicio del
módulo y las destruye al finalizar todas las pruebas en este archivo.
Debido a esto, los objetos creados en una prueba permanecen en la base de
datos para las pruebas posteriores dentro del mismo módulo. Si se desea
aislamiento completo por prueba, cambie el scope del fixture a "function"
o limpie explícitamente las tablas entre pruebas.
- Estas pruebas validan operaciones CRUD básicas y relaciones; no cubren
validaciones de negocio complejas ni migraciones de esquemas.
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
    """
    Fixture de preparación y limpieza de la base de datos para el módulo.

    Comportamiento:
    - Crea todas las tablas definidas en `Base` antes de ejecutar las pruebas.
    - Proporciona una sesión `db` ligada al engine en memoria.
    - Al finalizar el módulo, cierra la sesión y elimina las tablas creadas.

    Consideraciones:
    - El scope "module" permite reutilizar la misma estructura de tablas entre
    pruebas, lo que puede acelerar la ejecución pero comparte datos entre ellas.
    """
    # Crear tablas en el engine en memoria
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)

# -------------------------
# Tests User
# -------------------------
def test_create_user(setup_db):
    """
    Verifica que se pueda crear y persistir una instancia de User.

    - Se crea un User con email, password_hash y name.
    - Se confirma la persistencia mediante commit y refresh.
    - Se comprueba que se generó un id y que los campos coinciden.
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
    """
    Verifica la creación de un Board asociado a un User (owner).

    - Crea un User, lo persiste y crea un Board relacionado.
    - Comprueba que el board tenga id, owner correcto y nombre esperado.
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
    """
    Verifica la creación de una List vinculada a un Board.

    - Crea User y Board, luego crea una List con posición definida.
    - Comprueba id, relación con board y posición.
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
    """
    Verifica la creación de una Card y sus relaciones con Board, List y User.

    - Crea User, Board y List; luego crea la Card asignando created_by y responsible.
    - Comprueba que la tarjeta fue persistida y las relaciones apuntan a las entidades creadas.
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
    """
    Verifica la creación de una TimeEntry asociada a User y Card.

    - Crea User, Board, List y Card; luego crea una TimeEntry con fecha y horas.
    - Comprueba id, relaciones y valor de `hours`.
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
    """
    Verifica la creación de una relación BoardMember entre User y Board.

    - Crea User y Board; luego crea un BoardMember con rol (por ejemplo "admin").
    - Comprueba id, relaciones y el valor del rol.
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