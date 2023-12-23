from pydantic import BaseModel
import datetime


class PortfolioBase(BaseModel):
    name: str
    description: str | None = None


class PortfolioCreate(PortfolioBase):
    pass


class Portfolio(PortfolioBase):
    id: int
    user_id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime

    class Config:
        from_attributes = True
