from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import func
from enum import Enum as PyEnum
from app.database.database import Base
from datetime import datetime

class TransactionType(PyEnum):
    BUY = "buy"
    SELL = "sell"
    TRANSFER = "transfer"

class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement="auto", index=True)
    transaction_type: Mapped[TransactionType] = mapped_column(nullable=False)
    coin_symbol: Mapped[str] = mapped_column(nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    amount: Mapped[float] = mapped_column(nullable=False)
    price_per_token: Mapped[float] = mapped_column(nullable=False)
    portfolio_id: Mapped[int] = mapped_column(ForeignKey("portfolios.id"))
    created_at: Mapped[datetime] = mapped_column(default=func.now())
    updated_at: Mapped[datetime] = mapped_column(default=func.now(), onupdate=func.now())

    portfolio = relationship("Portfolio", back_populates="transactions")
    user = relationship("User", back_populates="transactions")