# =============================================================================
# database.py
# Purpose : Sets up the SQLAlchemy database connection for the TodoApp.
#           Provides the engine, session factory, and Base class used by all
#           other modules. Import from here — never re-create these elsewhere.
# =============================================================================

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# SQLite database file stored in the project root directory.
# The "sqlite:///./" prefix means "relative to the current working directory".
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:1999@127.0.0.1:3306/todoapplicationdatabase"


'''
The engine is the core connection to the database.
check_same_thread=False is required for SQLite when used with FastAPI,
because FastAPI can handle multiple threads and SQLite's default setting
would raise an error if the same connection is accessed from different threads.
'''
engine = create_engine(SQLALCHEMY_DATABASE_URL)


'''
sessionLocal is a factory for creating individual database sessions.
Each request gets its own session (opened at the start, closed at the end).
autocommit=False  → changes are not saved until we explicitly call commit()
autoflush=False   → SQLAlchemy won't auto-sync pending changes before queries
bind=engine       → links this session factory to our SQLite engine
'''
sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Base is the parent class for all ORM models (e.g. Users, Todos in models.py).
# SQLAlchemy uses it to track all table definitions and create/migrate them.
Base = declarative_base()
