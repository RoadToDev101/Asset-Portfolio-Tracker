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
from app.utils.api_response import TokenResponse
from app.schemas.access_token_schema import TokenWithData

load_dotenv()

router = APIRouter(prefix="/api/v1/auth", tags=["Authentication"])


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    response_model=TokenResponse[TokenWithData],
)
async def register(user: UserCreate, db: Session = Depends(get_db)):
    new_user = UserController.create_user(db, user=user)

    expires_delta = timedelta(days=float(os.getenv("JWT_LIFETIME_DAYS")))

    access_token = create_access_token(
        data={"sub": new_user.id},
        expires_delta=expires_delta,
    )

    return TokenResponse[TokenWithData].token_response(
        access_token=access_token,
        token_type="bearer",
        user_id=new_user.id,
        message="User registered successfully",
    )


@router.post(
    "/login",
    response_model=TokenResponse[TokenWithData],
    status_code=status.HTTP_200_OK,
)
async def login(
    response: Response,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
):
    authenticated_user = UserController.authenticate_user(
        db, form_data.username, form_data.password
    )

    refresh_token_lifespan = timedelta(days=float(os.getenv("JWT_LIFETIME_DAYS")))
    refresh_token = create_access_token(
        data={"sub": authenticated_user.user_id},
        expires_delta=refresh_token_lifespan,
    )

    # Set Refresh Token in HTTP-Only Cookie
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        max_age=refresh_token_lifespan.total_seconds(),  # Cookie lifespan in seconds
        expires=refresh_token_lifespan,  # Cookie expiry date
        secure=os.getenv("SECURE_COOKIE"),
    )

    return TokenResponse[TokenWithData].token_response(
        access_token=authenticated_user.access_token,
        token_type=authenticated_user.token_type,
        user_id=authenticated_user.user_id,
        message="User logged in successfully",
    )


@router.get(
    "/logout",
    status_code=status.HTTP_200_OK,
)
async def logout(response: Response):
    response.delete_cookie(key="refresh_token")
    return {"message": "User logged out successfully"}
