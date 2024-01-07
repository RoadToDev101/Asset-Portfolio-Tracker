from sqlalchemy import ForeignKey, Enum as SQLAlchemyEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import func
from app.database.database import Base
from datetime import datetime
from enum import Enum as PyEnum
import uuid
from app.models.portfolio_model import AssetType


class TransactionType(str, PyEnum):
    BUY = "buy"
    SELL = "sell"
    TRANSFER = "transfer"


class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        index=True,
    )
    description: Mapped[str] = mapped_column()
    transaction_type: Mapped[TransactionType] = mapped_column(
        SQLAlchemyEnum(TransactionType), nullable=False
    )
    asset_type: Mapped[AssetType] = mapped_column(
        SQLAlchemyEnum(AssetType), nullable=False
    )
    ticker: Mapped[str] = mapped_column(nullable=False)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    amount: Mapped[float] = mapped_column(nullable=False)
    currency: Mapped[str] = mapped_column(
        nullable=False
    )  # Assuming ISO 4217 currency codes
    unit_price: Mapped[float] = mapped_column(nullable=False)
    transaction_fee: Mapped[float] = mapped_column(nullable=False)
    portfolio_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("portfolios.id"), nullable=False, index=True
    )
    created_at: Mapped[datetime] = mapped_column(default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        default=func.now(), onupdate=func.now()
    )
    deleted_at: Mapped[datetime] = mapped_column(nullable=True)

    portfolio = relationship("Portfolio", back_populates="transactions")
    user = relationship("User", back_populates="transactions")
