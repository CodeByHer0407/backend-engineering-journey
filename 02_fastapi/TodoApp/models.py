# =============================================================================
# models.py
#
# Defines the SQLAlchemy ORM models used by the application.
# Each model represents a database table and its relationships.
# =============================================================================

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class Users(Base):
    """
    Represents the application's users.

    Stores authentication credentials and basic profile information.
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    email = Column(String(255), unique=True, nullable=False)
    username = Column(String(50), unique=True, nullable=False)

    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)

    hashed_password = Column(String(255), nullable=False)

    is_active = Column(Boolean, default=True, nullable=False)

    role = Column(String(20), nullable=False)

    phone_number = Column(String(10), nullable=False)

    # One user can own many todos
    todos = relationship("Todos", back_populates="owner_user")


class Todos(Base):
    """
    Represents a todo item created by a user.
    """

    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String(100), nullable=False)

    description = Column(String(500), nullable=False)

    priority = Column(Integer, nullable=False)

    complete = Column(Boolean, default=False, nullable=False)

    owner = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Reference back to the owning user
    owner_user = relationship("Users", back_populates="todos")