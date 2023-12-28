from sqlalchemy import ForeignKey, Enum as SQLAlchemyEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import func
from app.database.database import Base
from datetime import datetime
from enum import Enum as PyEnum


class TransactionType(PyEnum):
    BUY = "buy"
    SELL = "sell"
    TRANSFER = "transfer"


class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement="auto", index=True)
    transaction_type: Mapped[TransactionType] = mapped_column(
        SQLAlchemyEnum(TransactionType), nullable=False
    )
    coin_symbol: Mapped[str] = mapped_column(nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    amount: Mapped[float] = mapped_column(nullable=False)
    price_per_token: Mapped[float] = mapped_column(nullable=False)
    portfolio_id: Mapped[int] = mapped_column(
        ForeignKey("portfolios.id"), nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        default=func.now(), onupdate=func.now()
    )

    portfolio = relationship("Portfolio", back_populates="transactions")
    user = relationship("User", back_populates="transactions")
