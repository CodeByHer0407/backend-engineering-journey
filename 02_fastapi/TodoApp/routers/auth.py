# =============================================================================
# auth.py
#
# Handles user authentication, JWT token generation, registration,
# login, and template rendering.
# =============================================================================

import os
from datetime import datetime, timedelta, timezone
from typing import Annotated

from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy.orm import Session

from database import SessionLocal
from models import Users

load_dotenv()

# ---------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------

SECRET_KEY = os.getenv("SECRET_KEY")

if not SECRET_KEY:
    raise ValueError("SECRET_KEY environment variable is not set.")

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 20

bcrypt_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="/auth/token")

templates = Jinja2Templates(directory="templates")

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)

# ---------------------------------------------------------------------
# Request / Response Models
# ---------------------------------------------------------------------


class CreateUserRequest(BaseModel):
    email: EmailStr
    username: str = Field(min_length=3, max_length=50)
    first_name: str = Field(min_length=2, max_length=50)
    last_name: str = Field(min_length=2, max_length=50)
    password: str = Field(min_length=8)
    role: str = Field(min_length=2, max_length=20)
    phone_number: str = Field(pattern=r"^\d{10}$")


class Token(BaseModel):
    access_token: str
    token_type: str


# ---------------------------------------------------------------------
# Database Dependency
# ---------------------------------------------------------------------


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]

# ---------------------------------------------------------------------
# Template Pages
# ---------------------------------------------------------------------


@router.get("/login-page")
def render_login_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="login.html",
    )


@router.get("/register-page")
def render_register_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="register.html",
    )


# ---------------------------------------------------------------------
# Authentication Helpers
# ---------------------------------------------------------------------


def authenticate_user(
    username: str,
    password: str,
    db: Session,
) -> Users | None:
    """
    Verify a user's credentials.
    """
    user = db.query(Users).filter(Users.username == username).first()
    if user is None:
        return None
    if not bcrypt_context.verify(password, user.hashed_password):
        return None
    return user


def create_access_token(
    username: str,
    user_id: int,
    expires_delta: timedelta,
    role: str,
) -> str:
    """
    Create a signed JWT access token.
    """
    payload = {
        "sub": username,
        "id": user_id,
        "role": role,
    }
    expires = datetime.now(timezone.utc) + expires_delta
    payload.update({"exp": expires})
    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM,
    )


async def get_current_user(
    token: Annotated[str, Depends(oauth2_bearer)],
) -> dict:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials.",
    )
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
        )

        username: str | None = payload.get("sub")
        user_id: int | None = payload.get("id")
        user_role: str | None = payload.get("role")

        if username is None or user_id is None:
            raise credentials_exception

        return {
            "username": username,
            "id": user_id,
            "user_role": user_role,
        }

    except JWTError as exc:
        raise credentials_exception from exc


# ---------------------------------------------------------------------
# API Endpoints
# ---------------------------------------------------------------------


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
)
async def create_user(
    db: db_dependency,
    create_user_request: CreateUserRequest,
):

    existing_user = (
        db.query(Users)
        .filter(
            (Users.username == create_user_request.username)
            | (Users.email == create_user_request.email)
        )
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already exists.",
        )

    create_user_model = Users(
        email=create_user_request.email,
        username=create_user_request.username,
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        hashed_password=bcrypt_context.hash(create_user_request.password),
        is_active=True,
        role=create_user_request.role,
        phone_number=create_user_request.phone_number,
    )

    db.add(create_user_model)
    db.commit()
    db.refresh(create_user_model)

    return {"message": "User created successfully."}


@router.post(
    "/token",
    response_model=Token,
)
async def login_for_access_token(
    form_data: Annotated[
        OAuth2PasswordRequestForm,
        Depends(),
    ],
    db: db_dependency,
):
    user = authenticate_user(
        form_data.username,
        form_data.password,
        db,
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password.",
        )

    token = create_access_token(
        username=user.username,
        user_id=user.id,
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
        role=user.role,
    )

    return {
        "access_token": token,
        "token_type": "bearer",
    }
