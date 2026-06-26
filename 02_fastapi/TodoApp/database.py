# database.py
# Centralized database configuration for the application.

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URL = "postgresql://todoapp_db_r8j5_user:L4SPYjK52pJyNEur4SFZhwAwlSIlM3P3@dpg-d8vcco0g4nts738q1nk0-a.singapore-postgres.render.com/todoapp_db_r8j5"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# SQLite database file
#SQLALCHEMY_DATABASE_URL = "sqlite:///./todosapp.db"

# Engine: responsible for connecting SQLAlchemy to the database
#engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# Session factory: creates a new database session for each request
sessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base class for all ORM models (Users, Todos, etc.)
Base = declarative_base()