import bcrypt
from sqlalchemy.orm import Session
from schemas.user import UserCreate
from models.user import User as UserModel

class UserController():
    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> None | UserModel:
        return db.query(UserModel).filter(UserModel.id == user_id).first()

    @staticmethod
    def create_user(db: Session, user: UserCreate) -> None | str:
        # Hash the password
        hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        # Create the user
        db_user = UserModel(
            username=user.username,
            email=user.email,
            hashed_password=hashed_password
        )

        # Add the user to the database
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return "User created successfully"

# def get_users(db: Session, skip: int = 0, limit: int = 100) -> list[User]:
#     return db.query(User).offset(skip).limit(limit).all()

# def delete_user(db: Session, user: User) -> None:
#     db.delete(user)
#     db.commit()
#     return None