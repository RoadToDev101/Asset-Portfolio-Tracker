from fastapi import Depends, Request
from sqlalchemy.orm import Session
from app.database.db_config import SessionLocal
from app.controllers.user_controller import UserController
from app.schemas.user_schema import UserOut
from app.utils.jwt import decode_access_token
from jose import JWTError
from typing import Annotated
from uuid import UUID
from app.schemas.user_schema import UserRole
from app.utils.custom_exceptions import (
    CredentialsException,
    BadRequestException,
    ForbiddenException,
)

# from app.utils.access_token import Payload


def get_refresh_token(request: Request) -> str:
    refresh_token = request.cookies.get("refresh_token")
    if refresh_token is None:
        raise CredentialsException
    return refresh_token


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_current_user(
    token: Annotated[str, Depends(get_refresh_token)], db: Session = Depends(get_db)
) -> UserOut:
    try:
        payload = decode_access_token(token)
        user_id: UUID = payload.get("sub")
        if user_id is None:
            raise CredentialsException
        # token_data = Payload(user_id=user_id)  # Not needed if you only use user_id
    except JWTError:
        raise CredentialsException

    user = UserController.get_user_by_id(db, user_id=user_id)
    if user is None:
        raise CredentialsException
    return user


async def get_current_active_user(
    current_user: Annotated[UserOut, Depends(get_current_user)]
):
    if not current_user.is_active:
        raise BadRequestException("Inactive user")
    return current_user


async def get_current_active_admin(
    current_user: Annotated[UserOut, Depends(get_current_user)]
):
    if not current_user.is_active:
        raise BadRequestException("Inactive user")
    if current_user.role != UserRole.ADMIN:
        raise ForbiddenException()
    return current_user
