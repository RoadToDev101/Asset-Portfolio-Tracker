from sqlalchemy import ForeignKey, func, UniqueConstraint
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.database.database import Base
from datetime import datetime


class Portfolio(Base):
    __tablename__ = "portfolios"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        index=True,
    )
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column()
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        default=func.now(), onupdate=func.now()
    )

    owner = relationship("User", back_populates="portfolios")
    transactions = relationship(
        "Transaction", back_populates="portfolio", cascade="all, delete-orphan"
    )

    __table_args__ = (UniqueConstraint("name", "user_id", name="_name_user_uc"),)
