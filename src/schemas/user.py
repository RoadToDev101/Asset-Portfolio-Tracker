from pydantic import BaseModel, EmailStr, Field
import datetime
from .portfolio import Portfolio

class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr

class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=50)

class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime.datetime
    updated_at: datetime.datetime
    portfolios: list[Portfolio] = []

    class Config:
        from_attributes = True