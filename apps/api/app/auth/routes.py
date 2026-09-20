from __future__ import annotations

from fastapi import APIRouter, Depends
from psycopg import Connection

from app.db import get_db

from .dependencies import get_current_user
from .schemas import (
    LoginRequest,
    LoginResponse,
    RegisterRequest,
    UserResponse,
)
from .service import authenticate_user, register_user
from .tokens import create_access_token


router = APIRouter(
    prefix="/auth",
    tags=["authentication"],
)


@router.post("/register", response_model=UserResponse)
def register(
    request: RegisterRequest,
    db: Connection = Depends(get_db),
):
    user_id = register_user(
        db,
        email=request.email,
        name=request.name,
        password=request.password,
    )

    row = db.execute(
        """
        SELECT id, email, name, active
        FROM users
        WHERE id = %s
        """,
        (user_id,),
    ).fetchone()

    if row is None:
        raise RuntimeError("User was created but could not be loaded")

    return UserResponse(
        id=str(row[0]),
        email=row[1],
        name=row[2],
        active=row[3],
    )


@router.post("/login", response_model=LoginResponse)
def login(
    request: LoginRequest,
    db: Connection = Depends(get_db),
):
    user = authenticate_user(
        db,
        email=request.email,
        password=request.password,
    )

    token = create_access_token(
        user_id=user["id"],
    )

    return LoginResponse(
        access_token=token,
        user=UserResponse(**user),
    )


@router.get("/me", response_model=UserResponse)
def me(
    current_user=Depends(get_current_user),
    db: Connection = Depends(get_db),
):
    row = db.execute(
        """
        SELECT id, email, name, active
        FROM users
        WHERE id = %s
        """,
        (current_user.id,),
    ).fetchone()

    if row is None:
        from fastapi import HTTPException, status

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User no longer exists",
        )

    return UserResponse(
        id=str(row[0]),
        email=row[1],
        name=row[2],
        active=row[3],
    )