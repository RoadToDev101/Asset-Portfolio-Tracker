from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime
from database.database import Base

class Portfolio(Base):
    __tablename__ = "portfolios"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement="auto", index=True)
    name: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column(default=func.now())
    updated_at: Mapped[datetime] = mapped_column(default=func.now(), onupdate=func.now())

    owner = relationship("User", back_populates="portfolios")
    transactions = relationship("Transaction", back_populates="portfolio")