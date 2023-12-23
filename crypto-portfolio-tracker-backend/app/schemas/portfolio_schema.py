from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID


class PortfolioBase(BaseModel):
    name: str
    description: str | None = None


class PortfolioCreate(PortfolioBase):
    name: str = Field(..., min_length=3, max_length=50)
    description: str | None = Field(None, max_length=254)
    user_id: UUID = Field(...)


class PortfolioUpdate(PortfolioBase):
    name: str = Field(None, min_length=3, max_length=50)
    description: str | None = Field(None, max_length=254)


class PortfolioOut(PortfolioBase):
    id: int
    user_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
