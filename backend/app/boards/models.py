"""
Modelos ORM principales del sistema de gestión de tableros Kanban.

Este módulo define las tablas y relaciones para usuarios, tableros, listas,
tarjetas, registros de tiempo y membresías usando SQLAlchemy.
"""
from datetime import datetime, timezone
from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Date,
    DateTime,
    Boolean,
    Numeric,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship
from ..database import Base



class User(Base):
    """
    Modelo de usuario del sistema.

    Representa una cuenta con credenciales y relaciones hacia tableros,
    tarjetas y registros de tiempo.

    Campos principales:
        id (int): Identificador único del usuario.
        email (str): Correo único.
        password_hash (str): Contraseña encriptada.
        name (str): Nombre del usuario.
        role (str): Rol o tipo de usuario.
        created_at/updated_at (datetime): Fechas de registro y modificación.

    Relaciones:
        boards: Tableros de los que es propietario.
        created_cards: Tarjetas creadas por el usuario.
        responsible_cards: Tarjetas en las que es responsable.
        time_entries: Registros de tiempo asociados.
        board_memberships: Membresías en tableros.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    name = Column(String(100), nullable=True)
    role = Column(String(50), nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    # Relaciones
    boards = relationship("Board",back_populates="owner",cascade="all, delete-orphan",passive_deletes=True,)
    created_cards = relationship("Card",foreign_keys="Card.created_by_id",back_populates="created_by",)
    responsible_cards = relationship("Card",foreign_keys="Card.responsible_id",back_populates="responsible",)
    time_entries = relationship("TimeEntry",back_populates="user",cascade="all, delete-orphan",)
    board_memberships = relationship("BoardMember",back_populates="user",cascade="all, delete-orphan",)


class Board(Base):
    """
    Modelo de tablero Kanban.

    Representa un tablero donde los usuarios organizan listas y tarjetas.

    Campos principales:
        id (int): Identificador único de tablero.
        name (str): Nombre del tablero.
        user_id (int): Usuario propietario del tablero.
        created_at (datetime): Fecha de creación.
    
    Relaciones:
        owner: Usuario propietario.
        lists: Listas asociadas.
        cards: Tarjetas asociadas.
        members: Miembros del tablero.
    """
    __tablename__ = "boards"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    user_id = Column(Integer,ForeignKey("users.id", ondelete="CASCADE"),nullable=False,)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    # Relaciones
    owner = relationship("User", back_populates="boards")
    lists = relationship("List",back_populates="board",cascade="all, delete-orphan",passive_deletes=True,)
    cards = relationship("Card",back_populates="board",cascade="all, delete-orphan",passive_deletes=True,)
    members = relationship("BoardMember",back_populates="board", cascade="all, delete-orphan",passive_deletes=True,)


class List(Base):
    """
    Modelo de lista dentro de un tablero.

    Permite agrupar tarjetas por proceso, etapa o categoría.

    Campos principales:
        id (int): Identificador único de la lista.
        board_id (int): Tablero al que pertenece.
        name (str): Nombre de la lista.
        position (int): Posición en el tablero.
        created_at (datetime): Fecha de creación.

    Relaciones:
        board: Tablero al que pertenece.
        cards: Tarjetas dentro de la lista.
    """
    __tablename__ = "lists"

    id = Column(Integer, primary_key=True, index=True)
    board_id = Column(Integer,ForeignKey("boards.id", ondelete="CASCADE"),nullable=False,)
    name = Column(String(100), nullable=False)
    position = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    # Relaciones
    board = relationship("Board", back_populates="lists")
    cards = relationship("Card",back_populates="list",cascade="all, delete-orphan",passive_deletes=True,)


class Card(Base):
    """
    Modelo de tarjeta/do Kanban.

    Define tareas o ítems que pueden moverse entre listas y tableros.

    Campos principales:
        id (int): Identificador único de la tarjeta.
        board_id, list_id (int): Relación con tablero y lista.
        title (str): Título de la tarea.
        description (Text): Descripción detallada.
        due_date (Date): Fecha de entrega.
        responsible_id (int): Usuario responsable.
        created_by_id (int): Usuario creador.
        created_at/updated_at/completed_at: Tiempos de registro.
        position (int): Para orden en la lista.
        priority (str): Nivel de prioridad.
        archived (bool): Indica si está archivada.

    Relaciones:
        board: Tablero dueño.
        list: Lista actual.
        responsible: Usuario responsable.
        created_by: Usuario creador.
        time_entries: Registros de tiempo asociados.
    """

    __tablename__ = "cards"

    id = Column(Integer, primary_key=True, index=True)
    board_id = Column(Integer,ForeignKey("boards.id", ondelete="CASCADE"),nullable=False,)
    list_id = Column(Integer,ForeignKey("lists.id", ondelete="CASCADE"),nullable=False,)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    due_date = Column(Date, nullable=True)
    responsible_id = Column(Integer,ForeignKey("users.id"),nullable=True,)
    created_by_id = Column(Integer,ForeignKey("users.id"),nullable=False,)

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)
    completed_at = Column(DateTime, nullable=True)

    position = Column(Integer, nullable=False, default=0)
    priority = Column(String(20), nullable=True)
    archived = Column(Boolean, nullable=False, default=False)

    #codigo semana 3
    @property
    def order(self) -> int:
        """
        Alias lógico para exponer el orden de la tarjeta en la API.

        - La base de datos usa `position`
        - La API (Semana 3) usa `order`
        """
        return self.position



    # Relaciones
    board = relationship("Board", back_populates="cards")
    list = relationship("List", back_populates="cards")
    responsible = relationship("User",foreign_keys=[responsible_id],back_populates="responsible_cards",)
    created_by = relationship("User",foreign_keys=[created_by_id],back_populates="created_cards")
    time_entries = relationship("TimeEntry",back_populates="card",cascade="all, delete-orphan",passive_deletes=True,)
    labels = relationship("Label", back_populates="card", cascade="all, delete-orphan")
    subtasks = relationship("Subtask", back_populates="card", cascade="all, delete-orphan")


class Label(Base):
    """
    Modelo para etiquetas (Labels) de una tarjeta.
    """
    __tablename__ = "labels"

    id = Column(Integer, primary_key=True, index=True)
    card_id = Column(Integer, ForeignKey("cards.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(50), nullable=False)
    color = Column(String(20), nullable=True)  # Hex code or name

    card = relationship("Card", back_populates="labels")


class Subtask(Base):
    """
    Modelo para subtareas (Checklist) de una tarjeta.
    """
    __tablename__ = "subtasks"

    id = Column(Integer, primary_key=True, index=True)
    card_id = Column(Integer, ForeignKey("cards.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(200), nullable=False)
    completed = Column(Boolean, default=False, nullable=False)
    position = Column(Integer, default=0)

    card = relationship("Card", back_populates="subtasks")


class TimeEntry(Base):
    """
    Registro de tiempo invertido en una tarjeta.

    Permite cuantificar esfuerzos y generar historiales de trabajo.

    Campos principales:
        id (int): Identificador único.
        user_id (int): Usuario que registró el tiempo.
        card_id (int): Tarjeta asociada.
        date (Date): Fecha del registro.
        hours (Numeric): Horas trabajadas.
        note (Text): Notas adicionales.
        created_at (datetime): Fecha del registro.

    Relaciones:
        user: Usuario asociado.
        card: Tarjeta asociada.
    """
    __tablename__ = "time_entries"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer,ForeignKey("users.id"),nullable=False,)
    card_id = Column(Integer,ForeignKey("cards.id", ondelete="CASCADE"),nullable=False,)
    date = Column(Date, nullable=False)
    hours = Column(Numeric(5, 2), nullable=False)
    note = Column(Text, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime,default=lambda: datetime.now(timezone.utc),onupdate=lambda: datetime.now(timezone.utc),nullable=False,)#semana4

    # Relaciones
    user = relationship("User", back_populates="time_entries")
    card = relationship("Card", back_populates="time_entries")


class BoardMember(Base):
    """
    Asociación entre usuarios y tableros (membresías).

    Permite controlar roles y accesos de los usuarios a los tableros.

    Campos principales:
        id (int): Identificador único.
        board_id (int): Tablero asociado.
        user_id (int): Usuario asociado.
        role (str): Rol dentro del tablero.

    Restricciones:
        uq_board_user: Un usuario sólo puede estar una vez en cada tablero.

    Relaciones:
        board: Tablero al que pertenece la membresía.
        user: Usuario relacionado.
    """
    __tablename__ = "board_members"
    __table_args__ = (UniqueConstraint("board_id", "user_id", name="uq_board_user"),)

    id = Column(Integer, primary_key=True, index=True)
    board_id = Column(Integer,ForeignKey("boards.id", ondelete="CASCADE"),nullable=False,)
    user_id = Column(Integer,ForeignKey("users.id", ondelete="CASCADE"),nullable=False,)
    role = Column(String(50), nullable=True)

    # Relaciones
    board = relationship("Board", back_populates="members")
    user = relationship("User", back_populates="board_memberships")