from sqlalchemy import func
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import List
from datetime import datetime

from database.database import Base
from models.portfolio import Portfolio

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement="auto", index=True)
    username: Mapped[str] = mapped_column(unique=True, index=True)
    email: Mapped[str] = mapped_column(unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column()
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(default=func.now())
    updated_at: Mapped[datetime] = mapped_column(default=func.now(), onupdate=func.now())

    # portfolios: Mapped[List["Portfolio"]] = relationship(back_populates="owner")
    portfolios = relationship("Portfolio", back_populates="owner")