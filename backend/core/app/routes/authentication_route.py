import os
from typing import Annotated
from dotenv import load_dotenv
from app.utils.jwt import create_access_token
from datetime import timedelta
from fastapi import APIRouter, Depends, status, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.controllers.user_controller import UserController
from app.schemas.user_schema import UserCreate

load_dotenv()

router = APIRouter(prefix="/api/v1/auth", tags=["Authentication"])


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
)
async def register(user: UserCreate, response: Response, db: Session = Depends(get_db)):
    new_user = UserController.create_user(db, user=user)

    expires_delta = timedelta(days=float(os.getenv("JWT_LIFETIME_DAYS")))

    access_token = create_access_token(
        data={"sub": new_user.id},
        expires_delta=expires_delta,
    )

    # Set the HTTPOnly cookie with the access token
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        max_age=float(os.getenv("JWT_LIFETIME_DAYS")) * 24 * 60 * 60,
        expires=float(os.getenv("JWT_LIFETIME_DAYS")) * 24 * 60 * 60,
    )

    return {"message": "User registered successfully"}


@router.post(
    "/login",
    status_code=status.HTTP_200_OK,
)
async def login(
    response: Response,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
):
    access_token = UserController.authenticate_user(
        db, form_data.username, form_data.password
    )

    # Set the HTTPOnly cookie with the access token
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        max_age=float(os.getenv("JWT_LIFETIME_DAYS")) * 24 * 60 * 60,
        expires=float(os.getenv("JWT_LIFETIME_DAYS")) * 24 * 60 * 60,
    )

    return {"message": "User logged in successfully"}


@router.get(
    "/logout",
    status_code=status.HTTP_200_OK,
)
async def logout(response: Response):
    response.delete_cookie(key="access_token")
    return {"message": "User logged out successfully"}
