from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import func
from datetime import datetime
from models.portfolio import Portfolio
# from models.coin import Coin

from database.database import Base

class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement="auto", index=True)
    coin_id: Mapped[int] = mapped_column(ForeignKey("coins.id"))
    portfolio_id: Mapped[int] = mapped_column(ForeignKey("portfolios.id"))
    amount: Mapped[float] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(default=func.now())
    updated_at: Mapped[datetime] = mapped_column(default=func.now(), onupdate=func.now())

    coin = relationship("Coin", back_populates="transactions")
    portfolio = relationship("Portfolio", back_populates="transactions")