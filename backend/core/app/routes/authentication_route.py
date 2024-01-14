import os
from typing import Annotated
from dotenv import load_dotenv
from app.utils.jwt import create_access_token, decode_access_token
from datetime import timedelta
from fastapi import APIRouter, Depends, status, Response, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.controllers.user_controller import UserController
from app.schemas.user_schema import UserCreate
from app.schemas.api_response import TokenResponse
from app.schemas.access_token_schema import Payload
from app.utils.custom_exceptions import ForbiddenException, NotFoundException

load_dotenv()

router = APIRouter(prefix="/api/v1/auth", tags=["Authentication"])


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    response_model=TokenResponse[Payload],
)
async def register(user: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user.

    Args:
        user (UserCreate): The user data to be registered.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        TokenResponse[Payload]: The token response containing the access token, token type, user ID, and message.
    """
    new_user = UserController.create_user(db, user=user)

    expires_delta = timedelta(days=float(os.getenv("JWT_LIFETIME_DAYS")))

    access_token = create_access_token(
        data={"sub": new_user.id},
        expires_delta=expires_delta,
    )

    return TokenResponse[Payload].token_response(
        access_token=access_token,
        token_type="bearer",
        user_id=new_user.id,
        role=new_user.role,
        is_active=new_user.is_active,
        message="User registered successfully",
    )


@router.post(
    "/login",
    response_model=TokenResponse[Payload],
    status_code=status.HTTP_200_OK,
)
async def login(
    response: Response,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
):
    """
    Authenticate the user and generate access and refresh tokens.

    Args:
        response (Response): The response object.
        form_data (OAuth2PasswordRequestForm): The form data containing the username and password.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        TokenResponse[Payload]: The response containing the access token, token type, user ID, and message.
    """
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
        secure=bool(os.getenv("SECURE_COOKIE")),
    )

    return TokenResponse[Payload].token_response(
        access_token=authenticated_user.access_token,
        token_type=authenticated_user.token_type,
        user_id=authenticated_user.user_id,
        role=authenticated_user.role,
        is_active=authenticated_user.is_active,
        message="User logged in successfully",
    )


@router.get(
    "/refresh",
    response_model=TokenResponse[Payload],
    status_code=status.HTTP_200_OK,
)
async def refresh(
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    """
    Refreshes the access token by decoding the refresh token from the request cookies,
    creating a new access token, and setting the new refresh token in the HTTP-only cookie.

    Args:
        request (Request): The incoming request object.
        response (Response): The outgoing response object.

    Raises:
        NotFoundException: If the refresh token is not found in the request cookies.
        ForbiddenException: If the decoded refresh token is invalid.

    Returns:
        TokenResponse[Payload]: The response containing the new access token and user information.
    """
    # Get Refresh Token from Header
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise NotFoundException("Refresh token not found")

    # Decode Refresh Token
    decoded_refresh_token = decode_access_token(refresh_token)
    if not decoded_refresh_token:
        raise ForbiddenException

    # Get user information from decoded refresh token
    user_id = decoded_refresh_token["sub"]
    user = UserController.get_user_by_id(db, user_id)

    # Create new Access Token
    access_token_lifespan = timedelta(days=float(os.getenv("JWT_LIFETIME_DAYS")))
    access_token = create_access_token(
        data={"sub": decoded_refresh_token["sub"]},
        expires_delta=access_token_lifespan,
    )

    # Set new Refresh Token in HTTP-Only Cookie
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        max_age=access_token_lifespan.total_seconds(),  # Cookie lifespan in seconds
        expires=access_token_lifespan,  # Cookie expiry date
        secure=bool(os.getenv("SECURE_COOKIE")),
    )

    return TokenResponse[Payload].token_response(
        access_token=access_token,
        token_type="bearer",
        user_id=user.id,
        role=user.role,
        is_active=user.is_active,
        message="Access token refreshed successfully",
    )


@router.get(
    "/logout",
    status_code=status.HTTP_200_OK,
)
async def logout(response: Response):
    """
    Logout the user by deleting the refresh token cookie.

    Args:
        response (Response): The HTTP response object.

    Returns:
        dict: A dictionary containing the success message.
    """
    response.delete_cookie(key="refresh_token")
    return {"message": "User logged out successfully"}
