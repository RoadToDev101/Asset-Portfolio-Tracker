from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID
from .transaction_schema import TransactionOut
from typing import Optional, List
from app.models.portfolio_model import AssetType


class PortfolioBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=50)
    description: Optional[str] = Field(None, max_length=254)
    asset_type: AssetType = Field(...)


class PortfolioCreate(PortfolioBase):
    user_id: UUID = Field(...)


class PortfolioUpdate(PortfolioBase):
    name: Optional[str] = Field(None, min_length=3, max_length=50)
    description: Optional[str] = Field(None, max_length=254)


class PortfolioOut(BaseModel):
    id: UUID
    name: str
    description: Optional[str]
    user_id: UUID
    asset_type: AssetType
    created_at: datetime
    updated_at: datetime
    transactions: List[TransactionOut] = []

    class ConfigDict:
        from_attributes = True
