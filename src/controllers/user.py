import bcrypt
from sqlalchemy.orm import Session
from src.schemas.user import UserCreate, UserUpdate
from src.models.user import User as UserModel

class UserController():
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

    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> None | UserModel:
        return db.query(UserModel).filter(UserModel.id == user_id).first()

    @staticmethod
    def get_users(db: Session, skip: int = 0, limit: int = 10) -> list[UserModel]:
        return db.query(UserModel).offset(skip).limit(limit).all()

    @staticmethod
    def update_user_by_id(db: Session, user_id: int, user: UserUpdate) -> None | str:
        # Find the user
        db_user = db.query(UserModel).filter(UserModel.id == user_id).first()

        if db_user is None:
            return None

        # Update the user attributes
        if user.username:
            db_user.username = user.username
        if user.email:
            db_user.email = user.email
        if user.is_active is not None:
            db_user.is_active = user.is_active

        db.commit()
        db.refresh(db_user)
        return "User updated successfully"

    @staticmethod
    def delete_user_by_id(db: Session, user_id: int) -> None | str:
        db.query(UserModel).filter(UserModel.id == user_id).delete()
        db.commit()
        return "User deleted successfully"