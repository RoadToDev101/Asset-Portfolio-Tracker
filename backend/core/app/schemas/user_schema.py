from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from uuid import UUID
from typing import Optional
from app.models.user_model import UserRole


class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr = Field(..., max_length=254)
    role: UserRole = Field(default=UserRole.USER)
    is_active: Optional[bool] = True


class UserCreate(UserBase):
    password: str = Field(..., min_length=8)


class UserUpdate(UserBase):
    username: Optional[str] = Field(min_length=3, max_length=50)
    email: Optional[EmailStr] = Field(max_length=254)
    role: Optional[UserRole]
    is_active: Optional[bool]


class UserOut(BaseModel):
    id: UUID
    is_active: bool
    role: UserRole
    created_at: datetime
    updated_at: datetime

    class ConfigDict:
        orm_mode = True
        from_attributes = True
