# =============================================================================
# users.py
#
# Handles user profile operations such as retrieving profile information,
# changing passwords, and updating phone numbers.
# =============================================================================

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from passlib.context import CryptContext
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from database import SessionLocal
from models import Users

from .auth import get_current_user


router = APIRouter(prefix="/users", tags=["Users"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_db_user(db: Session, user_id: int) -> Users | None:
    """
    Retrieve the currently authenticated user from the database.
    """
    return (db.query(Users).filter(Users.id == user_id)).first()


class UserVerification(BaseModel):
    password: str = Field(min_length=8)
    new_password: str = Field(min_length=8)


class PhoneNumberRequest(BaseModel):
    phone_number: str = Field(pattern=r"^\d{10}$")


db_dependency = Annotated[Session, Depends(get_db)]
current_user_dependency = Annotated[dict, Depends(get_current_user)]
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.get("/", status_code=status.HTTP_200_OK)
async def get_user_info(user: current_user_dependency, db: db_dependency):
    return get_current_db_user(db, user["id"])


@router.put("/password", status_code=status.HTTP_200_OK)
async def change_password(
    user: current_user_dependency,
    db: db_dependency,
    user_verification: UserVerification,
):
    user_model = get_current_db_user(db, user["id"])
    if user_model is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found."
        )
    if not bcrypt_context.verify(
        user_verification.password, user_model.hashed_password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect current password.",
        )
    user_model.hashed_password = bcrypt_context.hash(user_verification.new_password)
    db.add(user_model)
    db.commit()
    db.refresh(user_model)
    return {"message": "Password updated successfully."}


@router.put("/phone-number", status_code=status.HTTP_200_OK)
async def change_phone_number(
    user: current_user_dependency, db: db_dependency, phone_request: PhoneNumberRequest
):
    user_model = get_current_db_user(db, user["id"])
    if user_model is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found."
        )

    user_model.phone_number = phone_request.phone_number
    db.add(user_model)
    db.commit()
    db.refresh(user_model)
    return {"message": "Phone number updated successfully."}
