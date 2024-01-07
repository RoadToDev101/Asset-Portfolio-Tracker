from pydantic import BaseModel, Field
from datetime import datetime
from app.models.transaction_model import TransactionType
from app.models.portfolio_model import AssetType
from uuid import UUID
from typing import Optional


class TransactionBase(BaseModel):
    description: Optional[str] = Field(None, max_length=254)
    transaction_type: TransactionType = Field(...)
    asset_type: AssetType = Field(...)
    ticker: str = Field(..., min_length=3, max_length=8)
    amount: float = Field(..., gt=0)
    currency: str = Field(..., min_length=3, max_length=3)  # ISO 4217 currency codes
    unit_price: float = Field(..., gt=0)
    transaction_fee: float = Field(..., ge=0)  # ge=0 allows for zero fee


class TransactionCreate(TransactionBase):
    user_id: UUID = Field(...)
    portfolio_id: UUID = Field(...)


class TransactionUpdate(BaseModel):
    description: Optional[str] = Field(None, max_length=254)
    transaction_type: Optional[TransactionType]
    ticker: Optional[str] = Field(None, min_length=3, max_length=8)
    amount: Optional[float] = Field(None, gt=0)
    currency: Optional[str] = Field(None, min_length=3, max_length=3)
    unit_price: Optional[float] = Field(None, gt=0)
    transaction_fee: Optional[float] = Field(None, ge=0)


class TransactionOut(BaseModel):
    id: UUID
    description: Optional[str]
    transaction_type: TransactionType
    asset_type: AssetType
    user_id: UUID
    portfolio_id: UUID
    ticker: str
    amount: float
    currency: str
    unit_price: float
    transaction_fee: float
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime]

    class ConfigDict:
        from_attributes = True
