from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Table, Text, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

# Tabla de asociación para la relación muchos a muchos entre Cards y Labels
card_labels = Table(
    "card_labels",
    Base.metadata,
    Column("card_id", Integer, ForeignKey("cards.id", ondelete="CASCADE"), primary_key=True),
    Column("label_id", Integer, ForeignKey("labels.id", ondelete="CASCADE"), primary_key=True),
)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)

    # Relaciones
    boards = relationship("Board", back_populates="owner")
    memberships = relationship("BoardMember", back_populates="user")
    time_entries = relationship("TimeEntry", back_populates="user")

class Board(Base):
    __tablename__ = "boards"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    description = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relaciones
    owner = relationship("User", back_populates="boards")
    lists = relationship("List", back_populates="board", cascade="all, delete-orphan")
    members = relationship("BoardMember", back_populates="board", cascade="all, delete-orphan")
    labels = relationship("Label", back_populates="board", cascade="all, delete-orphan")

class BoardMember(Base):
    __tablename__ = "board_members"

    id = Column(Integer, primary_key=True, index=True)
    board_id = Column(Integer, ForeignKey("boards.id", ondelete="CASCADE"))
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    role = Column(String, default="member")  # admin, member, viewer

    # Relaciones
    board = relationship("Board", back_populates="members")
    user = relationship("User", back_populates="memberships")

class List(Base):
    __tablename__ = "lists"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    position = Column(Integer, default=0)
    board_id = Column(Integer, ForeignKey("boards.id", ondelete="CASCADE"))

    # Relaciones
    board = relationship("Board", back_populates="lists")
    cards = relationship("Card", back_populates="list", cascade="all, delete-orphan", order_by="Card.position")

class Card(Base):
    __tablename__ = "cards"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    position = Column(Integer, default=0)
    list_id = Column(Integer, ForeignKey("lists.id", ondelete="CASCADE"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    due_date = Column(DateTime(timezone=True), nullable=True)

    # Relaciones
    list = relationship("List", back_populates="cards")
    time_entries = relationship("TimeEntry", back_populates="card", cascade="all, delete-orphan")
    labels = relationship("Label", secondary=card_labels, back_populates="labels")
    subtasks = relationship("Subtask", back_populates="card", cascade="all, delete-orphan")

class Label(Base):
    __tablename__ = "labels"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    color = Column(String, default="#000000")
    board_id = Column(Integer, ForeignKey("boards.id", ondelete="CASCADE"))

    # Relaciones
    board = relationship("Board", back_populates="labels")
    cards = relationship("Card", secondary=card_labels, back_populates="labels")

class Subtask(Base):
    __tablename__ = "subtasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    is_completed = Column(Boolean, default=False)
    position = Column(Integer, default=0)
    card_id = Column(Integer, ForeignKey("cards.id", ondelete="CASCADE"))

    # Relaciones
    card = relationship("Card", back_populates="subtasks")

class TimeEntry(Base):
    __tablename__ = "time_entries"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String)
    hours = Column(Integer, nullable=False)
    date = Column(DateTime(timezone=True), server_default=func.now())
    card_id = Column(Integer, ForeignKey("cards.id", ondelete="CASCADE"))
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relaciones
    card = relationship("Card", back_populates="time_entries")
    user = relationship("User", back_populates="time_entries")
