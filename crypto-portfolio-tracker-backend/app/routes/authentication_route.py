import os
from dotenv import load_dotenv
from app.utils.jwt import TokenCreationError, create_access_token
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.controllers.user_controller import UserController
from app.schemas.user_schema import UserCreate
from app.utils.api_response import ApiResponse
from app.utils.access_token import TokenWithData

load_dotenv()

router = APIRouter(prefix="/api/v1/auth", tags=["Authentication"])


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    response_model=ApiResponse[TokenWithData],
)
async def register(user: UserCreate, db: Session = Depends(get_db)):
    new_user = UserController.create_user(db, user=user)

    try:
        access_token = create_access_token(
            data={"sub": new_user.id},
            expires_delta=timedelta(minutes=int(os.getenv("JWT_LIFETIME_MINUTES"))),
        )
    except TokenCreationError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Failed to create access token",
        )
    return ApiResponse[TokenWithData].success_response(
        data={
            "access_token": access_token,
            "token_type": "bearer",
            "user_id": new_user.id,
        },
        message="User registered successfully",
    )


@router.post(
    "/login", response_model=ApiResponse[TokenWithData], status_code=status.HTTP_200_OK
)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    authenticated_user = UserController.authenticate_user(
        db, form_data.username, form_data.password
    )
    return ApiResponse[TokenWithData].success_response(
        data=authenticated_user, message="User logged in successfully"
    )
