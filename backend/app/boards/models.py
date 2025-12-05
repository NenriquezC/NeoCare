# app/models.py
from datetime import datetime

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
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    name = Column(String(100), nullable=True)
    role = Column(String(50), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relaciones
    boards = relationship(
        "Board",
        back_populates="owner",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    created_cards = relationship(
        "Card",
        foreign_keys="Card.created_by_id",
        back_populates="created_by",
    )

    responsible_cards = relationship(
        "Card",
        foreign_keys="Card.responsible_id",
        back_populates="responsible",
    )

    time_entries = relationship(
        "TimeEntry",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    board_memberships = relationship(
        "BoardMember",
        back_populates="user",
        cascade="all, delete-orphan",
    )


class Board(Base):
    __tablename__ = "boards"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relaciones
    owner = relationship("User", back_populates="boards")

    lists = relationship(
        "List",
        back_populates="board",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    cards = relationship(
        "Card",
        back_populates="board",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    members = relationship(
        "BoardMember",
        back_populates="board",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


class List(Base):
    __tablename__ = "lists"

    id = Column(Integer, primary_key=True, index=True)
    board_id = Column(
        Integer,
        ForeignKey("boards.id", ondelete="CASCADE"),
        nullable=False,
    )
    name = Column(String(100), nullable=False)
    position = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relaciones
    board = relationship("Board", back_populates="lists")

    cards = relationship(
        "Card",
        back_populates="list",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


class Card(Base):
    __tablename__ = "cards"

    id = Column(Integer, primary_key=True, index=True)
    board_id = Column(
        Integer,
        ForeignKey("boards.id", ondelete="CASCADE"),
        nullable=False,
    )
    list_id = Column(
        Integer,
        ForeignKey("lists.id", ondelete="CASCADE"),
        nullable=False,
    )
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    due_date = Column(Date, nullable=True)

    responsible_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=True,
    )
    created_by_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
    )

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    completed_at = Column(DateTime, nullable=True)

    position = Column(Integer, nullable=False, default=0)
    priority = Column(String(20), nullable=True)
    archived = Column(Boolean, nullable=False, default=False)

    # Relaciones
    board = relationship("Board", back_populates="cards")
    list = relationship("List", back_populates="cards")

    responsible = relationship(
        "User",
        foreign_keys=[responsible_id],
        back_populates="responsible_cards",
    )

    created_by = relationship(
        "User",
        foreign_keys=[created_by_id],
        back_populates="created_cards",
    )

    time_entries = relationship(
        "TimeEntry",
        back_populates="card",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


class TimeEntry(Base):
    __tablename__ = "time_entries"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
    )
    card_id = Column(
        Integer,
        ForeignKey("cards.id", ondelete="CASCADE"),
        nullable=False,
    )
    date = Column(Date, nullable=False)
    hours = Column(Numeric(5, 2), nullable=False)
    note = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relaciones
    user = relationship("User", back_populates="time_entries")
    card = relationship("Card", back_populates="time_entries")


class BoardMember(Base):
    __tablename__ = "board_members"
    __table_args__ = (
        UniqueConstraint("board_id", "user_id", name="uq_board_user"),
    )

    id = Column(Integer, primary_key=True, index=True)
    board_id = Column(
        Integer,
        ForeignKey("boards.id", ondelete="CASCADE"),
        nullable=False,
    )
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    role = Column(String(50), nullable=True)

    # Relaciones
    board = relationship("Board", back_populates="members")
    user = relationship("User", back_populates="board_memberships")