# =============================================================================
# todos.py
#
# Handles todo CRUD operations and template rendering for authenticated users.
# =============================================================================

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path, Request, status
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse

from database import SessionLocal
from models import Todos

from .auth import get_current_user

templates = Jinja2Templates(directory="templates")

router = APIRouter(prefix="/todos", tags=["Todos"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_user_todo(
    db: Session,
    todo_id: int,
    owner_id: int,
) -> Todos | None:
    """
    Retrieve a todo that belongs to the authenticated user.
    """
    return db.query(Todos).filter(Todos.id == todo_id, Todos.owner == owner_id).first()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


class TodoRequest(BaseModel):
    title: str = Field(min_length=3, max_length=100)
    description: str = Field(min_length=3, max_length=500)
    priority: int = Field(gt=0, lt=6)
    complete: bool


def redirect_to_login():
    response = RedirectResponse(
        url="/auth/login-page", status_code=status.HTTP_302_FOUND
    )
    response.delete_cookie("access_token")
    return response


async def get_template_user(request: Request):
    token = request.cookies.get("access_token")
    return await get_current_user(token)


# ---------------------------------------------------------------------
# Template Pages
# ---------------------------------------------------------------------


@router.get("/todo-page")
async def render_todos_page(request: Request, db: db_dependency):
    try:
        user = await get_template_user(request)
        todos = db.query(Todos).filter(Todos.owner == user["id"]).all()

        return templates.TemplateResponse(
            request=request, name="todo.html", context={"todos": todos, "user": user}
        )
    except Exception:
        return redirect_to_login()


@router.get("/add-todo-page")
async def render_add_todo_page(request: Request):
    try:
        user = await get_template_user(request)
        return templates.TemplateResponse(
            request=request, name="add-todo.html", context={"user": user}
        )
    except Exception:
        return redirect_to_login()


@router.get("/edit-todo-page/{todo_id}")
async def render_edit_todo_page(request: Request, todo_id: int, db: db_dependency):
    try:
        user = await get_template_user(request)
        todo_model = get_user_todo(
            db,
            todo_id,
            user["id"],
        )
        if todo_model is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found."
            )
        return templates.TemplateResponse(
            request=request,
            name="edit-todo.html",
            context={
                "user": user,
                "todo": todo_model,
            },
        )
    except Exception:
        return redirect_to_login()


# ---------------------------------------------------------------------
# API Endpoints
# ---------------------------------------------------------------------


@router.get("/")
async def read_all_todos(user: user_dependency, db: db_dependency):
    owner_id = user["id"]
    return db.query(Todos).filter(Todos.owner == owner_id).all()


@router.get("/todo/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo(
    user: user_dependency,
    db: db_dependency,
    todo_id: int = Path(gt=0, description="Todo ID"),
):
    todo_model = get_user_todo(
        db,
        todo_id,
        user["id"],
    )
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, detail="Todo not found!")


@router.post("/todo/", status_code=status.HTTP_201_CREATED)
async def create_todo(
    user: user_dependency, db: db_dependency, todo_request: TodoRequest
):
    todo_model = Todos(**todo_request.model_dump(), owner=user["id"])
    db.add(todo_model)
    db.commit()
    db.refresh(todo_model)
    return todo_model


@router.put("/todo/{todo_id}", status_code=status.HTTP_200_OK)
async def update_todo(
    user: user_dependency,
    db: db_dependency,
    todo_request: TodoRequest,
    todo_id: int = Path(gt=0, description="Todo ID"),
):
    todo_model = get_user_todo(
        db,
        todo_id,
        user["id"],
    )
    if todo_model is None:
        raise HTTPException(
            status_code=404, detail="Todo not found, try a different input."
        )
    todo_model.title = todo_request.title
    todo_model.description = todo_request.description
    todo_model.priority = todo_request.priority
    todo_model.complete = todo_request.complete

    db.add(todo_model)
    db.commit()
    db.refresh(todo_model)
    return todo_model


@router.delete("/todo/{todo_id}", status_code=status.HTTP_200_OK)
async def delete_todo(
    user: user_dependency,
    db: db_dependency,
    todo_id: int = Path(gt=0, description="Todo ID"),
):
    todo_model = get_user_todo(
        db,
        todo_id,
        user["id"],
    )
    if todo_model is None:
        raise HTTPException(
            status_code=404, detail="Todo not found. Try with a different input!"
        )
    db.delete(todo_model)
    db.commit()
    return {"message": "Todo deleted successfully."}
