from sqlalchemy import func, Enum as SQLAlchemyEnum
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
from app.database.database import Base
from datetime import datetime
import uuid
from enum import Enum as PyEnum


class UserRole(str, PyEnum):
    USER = "user"
    ADMIN = "admin"


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        index=True,
    )
    username: Mapped[str] = mapped_column(unique=True, index=True)
    email: Mapped[str] = mapped_column(unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column()
    is_active: Mapped[bool] = mapped_column(default=True)
    role: Mapped[UserRole] = mapped_column(SQLAlchemyEnum(UserRole), nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        default=func.now(), onupdate=func.now()
    )

    portfolios = relationship("Portfolio", back_populates="owner")
    transactions = relationship("Transaction", back_populates="user")
