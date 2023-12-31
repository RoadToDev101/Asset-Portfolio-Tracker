from typing import List
from passlib.context import CryptContext
from psycopg2.errors import UniqueViolation
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session
from app.schemas.user_schema import UserCreate, UserUpdate, UserOut
from app.models.user_model import User as UserModel
from app.utils.access_token import TokenWithData
import datetime
from app.utils.jwt import create_access_token
from uuid import UUID
import logging
from app.utils.common_utils import remove_private_attributes
from app.utils.custom_exceptions import (
    CredentialsException,
    NotFoundException,
    BadRequestException,
)
import os
from dotenv import load_dotenv

load_dotenv()

logging.getLogger("passlib").setLevel(logging.ERROR)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


class UserController:
    @staticmethod
    def authenticate_user(db: Session, username: str, password: str) -> TokenWithData:
        user = db.query(UserModel).filter(UserModel.username == username).first()

        if not user:
            raise NotFoundException("User not found. Please register")
        if not verify_password(password, user.hashed_password):
            raise CredentialsException("Incorrect username or password")

        access_token_expires = datetime.timedelta(
            days=float(os.getenv("JWT_LIFETIME_DAYS"))
        )
        access_token = create_access_token(
            data={"sub": user.id}, expires_delta=access_token_expires
        )

        token_data = TokenWithData(
            access_token=access_token, token_type="bearer", user_id=user.id
        )
        return token_data

    @staticmethod
    def create_user(db: Session, user: UserCreate) -> UserOut:
        # Hash the password
        hashed_password = get_password_hash(user.password)

        # Create the user
        new_user = UserModel(
            username=user.username,
            email=user.email,
            hashed_password=hashed_password,
            role=user.role,
        )

        # Add the user to the database
        db.add(new_user)

        try:
            db.commit()
            db.refresh(new_user)
        except IntegrityError as e:
            db.rollback()  # Roll back the transaction on error
            if isinstance(e.orig, UniqueViolation):
                raise BadRequestException("Username or email already exists")
            else:
                raise BadRequestException(f"Failed to create user: {e.orig}")

        user_dict = remove_private_attributes(
            new_user
        )  # Remove private attributes from the user object

        user_out = UserOut.model_validate(user_dict)

        return user_out

    @staticmethod
    def get_user_by_id(db: Session, user_id: UUID) -> UserOut:
        user = db.query(UserModel).get(user_id)
        if user is None:
            raise NotFoundException("User not found")
        user_dict = remove_private_attributes(user)
        user_out = UserOut.model_validate(user_dict)
        return user_out

    @staticmethod
    def get_users(db: Session, skip: int = 0, limit: int = 10) -> List[UserOut]:
        try:
            users = db.query(UserModel).offset(skip).limit(limit).all()
            results = []
            for user in users:
                user_dict = remove_private_attributes(user)
                user_out = UserOut.model_validate(user_dict)
                results.append(user_out)
            return results
        except SQLAlchemyError:
            raise BadRequestException("Failed to retrieve users")

    @staticmethod
    def update_user_by_id(db: Session, user_id: UUID, user: UserUpdate) -> UserOut:
        db_user = db.query(UserModel).get(user_id)
        if db_user is None:
            raise NotFoundException("User not found")

        # Update the user attributes
        if user.username:
            db_user.username = user.username
        if user.email:
            db_user.email = user.email
        if user.is_active is not None:
            db_user.is_active = user.is_active
        if user.role and (db_user.role != "user"):
            db_user.role = user.role

        try:
            db.commit()
            db.refresh(db_user)
        except IntegrityError as e:
            db.rollback()
            if isinstance(e.orig, UniqueViolation):
                raise BadRequestException("Username or email already exists")
            else:
                raise BadRequestException(f"Failed to update user: {e.orig}")
        user_dict = remove_private_attributes(db_user)
        user_out = UserOut.model_validate(user_dict)

        return user_out

    @staticmethod
    def delete_user_by_id(db: Session, user_id: UUID) -> str:
        user = db.query(UserModel).get(user_id)
        if user is None:
            raise NotFoundException("User not found")

        db.delete(user)
        try:
            db.commit()
        except SQLAlchemyError:
            db.rollback()
            raise BadRequestException("Failed to delete user")
        return "User deleted successfully"
