# database.py
# Centralized database configuration for the application.

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# SQLite database file
SQLALCHEMY_DATABASE_URL = "sqlite:///./todosapp.db"

# Engine: responsible for connecting SQLAlchemy to the database
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Session factory: creates a new database session for each request
sessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base class for all ORM models (Users, Todos, etc.)
Base = declarative_base()