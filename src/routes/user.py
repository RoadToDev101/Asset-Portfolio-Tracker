from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy.orm import Session
from src.dependencies import get_db
from src.controllers.user import UserController
from src.schemas.user import UserCreate, UserUpdate, User as UserSchema
from src.models.user import User as UserModel
from src.utils.pagination import Pagination

router = APIRouter()

@router.post("/users")
async def sign_up(user: UserCreate, db: Session = Depends(get_db)):
    return {"message": UserController.create_user(db, user=user)}

@router.get("/users/{user_id}", response_model=UserSchema)
async def get_user(user_id: int = Path(gt=0), db: Session = Depends(get_db)):
    db_user = UserController.get_user_by_id(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.get("/users", response_model=Pagination[UserSchema])
async def get_all_users(page: int = Query(gt=0), page_size: int = Query(gt=0), db: Session = Depends(get_db)):
    skip = (page - 1) * page_size
    users = UserController.get_users(db, skip=skip, limit=page_size)
    total = db.query(UserModel).count()
    return Pagination[UserSchema].create(users, page, page_size, total)

@router.patch("/users/{user_id}")
async def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    db_user = UserController.get_user_by_id(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": UserController.update_user_by_id(db, user_id=user_id, user=user)}

@router.delete("/users/{user_id}")
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = UserController.get_user_by_id(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": UserController.delete_user_by_id(db, user_id=user_id)}
