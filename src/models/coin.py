from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.transaction import Transaction

from database.database import Base

class Coin(Base):
    __tablename__ = "coins"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement="auto", index=True)
    name: Mapped[str] = mapped_column()
    symbol: Mapped[str] = mapped_column(unique=True, index=True)

    transactions = relationship("Transaction", back_populates="coin")