from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.controllers.user_controller import UserController
from app.schemas.user_schema import UserCreate, UserUpdate, UserOut
from app.models.user_model import User as UserModel
from app.utils.pagination import Pagination
from app.utils.jwt import create_access_token
from datetime import timedelta
from app.dependencies import get_current_user
from uuid import UUID
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()


@router.post("/register")
async def register(user: UserCreate, db: Session = Depends(get_db)):
    new_user = UserController.create_user(db, user=user)
    if new_user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to register user"
        )
    access_token_expires = timedelta(
        minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
    )
    access_token = create_access_token(
        data={"sub": new_user.id}, expires_delta=access_token_expires
    )
    if access_token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Failed to register user"
        )
    return {"access_token": access_token, "token_type": "bearer", "user": new_user}


@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    authenticated_user = UserController.authenticate_user(
        db, form_data.username, form_data.password
    )
    if not authenticated_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return authenticated_user


@router.get("/users/{user_id}", response_model=UserOut)
async def get_user(
    user_id: UUID,
    db: Session = Depends(get_db),
    current_user: UserOut = Depends(get_current_user),
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions"
        )
    user = UserController.get_user_by_id(db, user_id=user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user


@router.get("/users", response_model=Pagination[UserOut])
async def get_all_users(
    page: int = Query(gt=0),
    page_size: int = Query(gt=0),
    db: Session = Depends(get_db),
    current_user: UserOut = Depends(get_current_user),
):
    skip = (page - 1) * page_size
    users = UserController.get_users(db, skip=skip, limit=page_size)
    if users is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Users not found"
        )
    total = db.query(UserModel).count()
    return Pagination[UserOut].create(users, page, page_size, total)


@router.patch("/users/{user_id}")
async def update_user(
    user_id: UUID,
    user: UserUpdate,
    db: Session = Depends(get_db),
    current_user: UserOut = Depends(get_current_user),
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions"
        )
    db_user = UserController.get_user_by_id(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return {"message": UserController.update_user_by_id(db, user_id=user_id, user=user)}


@router.delete("/users/{user_id}")
async def delete_user(
    user_id: UUID,
    db: Session = Depends(get_db),
    current_user: UserOut = Depends(get_current_user),
):
    # if current_user.id != user_id:
    #     raise HTTPException(status_code=403, detail="Not enough permissions")
    db_user = UserController.get_user_by_id(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return {"message": UserController.delete_user_by_id(db, user_id=user_id)}
