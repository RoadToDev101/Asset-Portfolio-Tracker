from pydantic import BaseModel
from datetime import datetime
from app.models.transaction_model import TransactionType
from uuid import UUID


class TransactionBase(BaseModel):
    transaction_type: TransactionType
    coin_symbol: str
    amount: float
    price_per_token: float


class TransactionCreate(TransactionBase):
    pass


class TransactionOut(TransactionBase):
    id: int
    user_id: UUID
    portfolio_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
