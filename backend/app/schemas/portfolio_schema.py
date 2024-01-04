from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID
from .transaction_schema import TransactionOut
from typing import Optional, List


class PortfolioBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=50)
    description: Optional[str] = Field(None, max_length=254)


class PortfolioCreate(PortfolioBase):
    user_id: UUID = Field(...)


class PortfolioUpdate(PortfolioBase):
    name: Optional[str] = Field(None, min_length=3, max_length=50)
    description: Optional[str] = Field(None, max_length=254)


class PortfolioOut(BaseModel):
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime
    transactions: List[TransactionOut] = []

    class ConfigDict:
        from_attributes = True
