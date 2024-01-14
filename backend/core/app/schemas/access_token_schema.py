from pydantic import BaseModel
from uuid import UUID
from app.models.user_model import UserRole


class Token(BaseModel):
    access_token: str
    token_type: str


class Payload(Token):
    user_id: UUID
    role: UserRole
    is_active: bool
