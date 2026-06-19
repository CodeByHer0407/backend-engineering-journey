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

    id = Column(Integer, primary_key=True, index=True)  
    email = Column(String, unique=True)                  
    username = Column(String, unique=True)               
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)                     
    is_active = Column(Boolean, default=True)            
    role = Column(String)                           
    phone_number = Column(String(10))


class Todos(Base):
    """
    Represents the 'todos' table.
    Each todo item is owned by a user via the 'owner' foreign key.
    """
    __tablename__ = 'todos'

    id = Column(Integer, primary_key=True, index=True)   
    title = Column(String)                               
    description = Column(String)                         
    priority = Column(Integer)                           
    complete = Column(Boolean)                           
    owner = Column(Integer, ForeignKey("users.id"))      
                                                         