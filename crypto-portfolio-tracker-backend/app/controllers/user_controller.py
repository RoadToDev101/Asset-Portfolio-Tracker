import bcrypt
from psycopg2.errors import UniqueViolation
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.schemas.user_schema import UserCreate, UserUpdate, UserOut
from app.models.user_model import User as UserModel
import datetime
from app.utils.jwt import create_access_token
from fastapi import HTTPException, status


class UserController:
    @staticmethod
    def authenticate_user(db: Session, username: str, password: str):
        user = db.query(UserModel).filter(UserModel.username == username).first()
        if not user or not bcrypt.checkpw(
            password.encode("utf-8"), user.hashed_password.encode("utf-8")
        ):
            return None
        access_token_expires = datetime.timedelta(minutes=30)
        access_token = create_access_token(
            data={"sub": user.id}, expires_delta=access_token_expires
        )
        user_out = UserOut.model_validate(user)
        return {"access_token": access_token, "token_type": "bearer", "user": user_out}

    @staticmethod
    def create_user(db: Session, user: UserCreate) -> UserOut:
        # Check if the user already exists
        existing_user = (
            db.query(UserModel)
            .filter(
                (UserModel.username == user.username) | (UserModel.email == user.email)
            )
            .first()
        )

        if existing_user is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username or email already exists",
            )

        # Hash the password
        hashed_password = bcrypt.hashpw(
            user.password.encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8")

        # Create the user
        new_user = UserModel(
            username=user.username, email=user.email, hashed_password=hashed_password
        )

        # Add the user to the database
        db.add(new_user)

        try:
            db.commit()
        except IntegrityError as e:
            db.rollback()  # Roll back the transaction on error
            if isinstance(e.orig, UniqueViolation):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Username or email already exists",
                )
            else:
                raise  # Re-raise the exception if it's not a UniqueViolation

        db.refresh(
            new_user
        )  # Populate the new_user with all fields including id, created_at, etc.

        user_out = UserOut.model_validate(
            new_user
        )  # Convert the SQLAlchemy model to a Pydantic model

        return user_out

    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> None | UserOut:
        return db.query(UserModel).filter(UserModel.id == user_id).first()

    @staticmethod
    def get_users(db: Session, skip: int = 0, limit: int = 10) -> list[UserOut]:
        return db.query(UserModel).offset(skip).limit(limit).all()

    @staticmethod
    def update_user_by_id(
        db: Session, user_id: int, user: UserUpdate
    ) -> None | UserOut:
        db_user = db.query(UserModel).filter(UserModel.id == user_id).first()

        if db_user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )

        try:
            # Update the user attributes
            if user.username:
                db_user.username = user.username
            if user.email:
                db_user.email = user.email
            if user.is_active is not None:
                db_user.is_active = user.is_active

            db.commit()
        except IntegrityError as e:
            db.rollback()
            if isinstance(e.orig, UniqueViolation):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Username or email already exists",
                )
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Failed to update user",
                )

        db.refresh(db_user)

        user_out = UserOut.model_validate(db_user)
        return user_out

    @staticmethod
    def delete_user_by_id(db: Session, user_id: int) -> None | str:
        db.query(UserModel).filter(UserModel.id == user_id).delete()
        db.commit()
        return "User deleted successfully"
