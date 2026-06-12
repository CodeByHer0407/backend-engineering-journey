from fastapi import Depends, HTTPException, Path, status, APIRouter
from sqlalchemy.orm import Session
from models import Todos
from typing import Annotated
from database import sessionLocal
from pydantic import BaseModel, Field
from routers import auth
from .auth import get_current_user

router = APIRouter()


def get_db():
    db = sessionLocal()
    try:
        yield db 
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


class TodoRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    priority: int = Field(gt=0, lt=6)
    complete: bool 


@router.get("/")
async def read_all(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication failed.")
    return db.query(Todos).filter(Todos.owner == user.get("id")).all()


@router.get("/todo/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication failed.")
    todo_model = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner == user.get('id')).first()
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, detail="Todo not found!") 


@router.post("/todo/", status_code=status.HTTP_201_CREATED)
async def create_todo(user: user_dependency, db: db_dependency, todo_request: TodoRequest):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication failed.")
    todo_model = Todos(**todo_request.model_dump(), owner= user.get('id'))
    db.add(todo_model)
    db.commit()
    db.refresh(todo_model)
    return todo_model


@router.put("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(user: user_dependency, db: db_dependency, todo_request: TodoRequest, todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication failed.")
    todo_model = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner == user.get("id")).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo not found, try a different input.")
    todo_model.title = todo_request.title
    todo_model.description = todo_request.description
    todo_model.priority = todo_request.priority
    todo_model.complete = todo_request.complete

    db.add(todo_model)
    db.commit()


@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(user: user_dependency, db: db_dependency, todo_request: TodoRequest, todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication failed.")
    todo_model = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner == user.get("id")).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo not found. Try with a different input!")
    db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner == user.get("id")).delete()
    db.commit()