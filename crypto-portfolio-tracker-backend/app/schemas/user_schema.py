from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from .portfolio_schema import PortfolioOut
from uuid import UUID


class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr = Field(..., max_length=254)


class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=50)


class UserUpdate(UserBase):
    username: str = Field(None, min_length=3, max_length=50)
    email: EmailStr = Field(None, max_length=254)
    is_active: bool = Field(None)


class UserOut(UserBase):
    id: UUID
    is_active: bool
    created_at: datetime
    updated_at: datetime
    portfolios: list[PortfolioOut] = []

    class Config:
        from_attributes = True
