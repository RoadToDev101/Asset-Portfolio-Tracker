from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from .portfolio_schema import Portfolio


class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr = Field(..., max_length=254)


class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=50)


class UserUpdate(UserBase):
    is_active: bool = Field(None)


class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    portfolios: list[Portfolio] = []

    class Config:
        from_attributes = True
