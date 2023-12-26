from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.database.database import SessionLocal
from app.controllers.user_controller import UserController
from app.schemas.user_schema import UserOut
from app.utils.jwt import decode_access_token
from app.utils.access_token import TokenWithData
from jose import JWTError
from typing import Annotated
from uuid import UUID

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)
):
    try:
        payload = decode_access_token(token)
        user_id: UUID = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        # token_data = TokenWithData(user_id=user_id)  # Not needed if you only use user_id
    except JWTError:
        raise credentials_exception

    user = UserController.get_user_by_id(db, user_id=user_id)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[UserOut, Depends(get_current_user)]
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
