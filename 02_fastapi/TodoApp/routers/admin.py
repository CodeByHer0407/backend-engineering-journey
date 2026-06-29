# =============================================================================
# admin.py
#
# Admin-only endpoints for managing todo items.
# =============================================================================

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path, status
from sqlalchemy.orm import Session

from database import SessionLocal
from models import Todos

from .auth import get_current_user

router = APIRouter(prefix="/admin", tags=["Admin"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_todo(db: Session, todo_id: int) -> Todos | None:
    """
    Retrieve a todo by its ID.
    """
    return db.query(Todos).filter(Todos.id == todo_id).first()


def verify_admin(user: dict) -> None:
    """
    Ensure the authenticated user has administrator privileges.
    """
    if user.get("user_role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized."
        )


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


@router.get("/todo", status_code=status.HTTP_200_OK)
async def read_all_todos(user: user_dependency, db: db_dependency):
    verify_admin(user)
    return db.query(Todos).all()


@router.delete("/todo/{todo_id}", status_code=status.HTTP_200_OK)
async def delete_todo(
    user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)
):
    verify_admin(user)
    todo_model = get_todo(db, todo_id)
    if todo_model is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found"
        )
    db.delete(todo_model)
    db.commit()
    return {"message": "Todo deleted successfully."}
