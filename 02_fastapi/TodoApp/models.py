# =============================================================================
# models.py
# Purpose : Defines the database schema using SQLAlchemy ORM models.
#           Each class maps to a table in todosapp.db. Column definitions
#           here drive both table creation and Python-level data access.
# =============================================================================


from database import Base 
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey


class Users(Base):
    """
    Represents the 'users' table.
    Stores authentication credentials and basic profile info for each user.
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)  # Auto-incrementing unique ID
    email = Column(String, unique=True)                  # Must be unique across all users
    username = Column(String, unique=True)               # Must be unique across all users
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)                     # Stored as a bcrypt hash, never plain text
    is_active = Column(Boolean, default=True)            # Soft-disable a user without deleting them
    role = Column(String)                                # e.g. "admin" or "user" — controls permissions


class Todos(Base):
    """
    Represents the 'todos' table.
    Each todo item is owned by a user via the 'owner' foreign key.
    """
    __tablename__ = 'todos'

    id = Column(Integer, primary_key=True, index=True)   # Auto-incrementing unique ID
    title = Column(String)                               # Short name for the todo
    description = Column(String)                         # Longer details (optional)
    priority = Column(Integer)                           # e.g. 1 (low) to 5 (high)
    complete = Column(Boolean)                           # True once the task is done
    owner = Column(Integer, ForeignKey("users.id"))      # Links this todo to a specific user
                                                         # Enforces referential integrity at DB level