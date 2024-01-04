from pydantic import BaseModel, Field
from datetime import datetime
from app.models.transaction_model import TransactionType
from uuid import UUID
from typing import Optional


class TransactionBase(BaseModel):
    transaction_type: TransactionType = Field(...)
    coin_symbol: str = Field(..., min_length=3, max_length=8)
    amount: float = Field(..., gt=0)
    price_per_token: float = Field(..., gt=0)


class TransactionCreate(TransactionBase):
    user_id: UUID = Field(...)
    portfolio_id: UUID = Field(...)


class TransactionUpdate(TransactionBase):
    transaction_type: Optional[TransactionType]
    coin_symbol: Optional[str] = Field(min_length=3, max_length=8)
    amount: Optional[float] = Field(gt=0)
    price_per_token: Optional[float] = Field(gt=0)


class TransactionOut(BaseModel):
    id: UUID
    transaction_type: TransactionType
    user_id: UUID
    portfolio_id: UUID
    created_at: datetime
    updated_at: datetime

    class ConfigDict:
        from_attributes = True
