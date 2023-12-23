from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from app.schemas.portfolio_schema import PortfolioCreate, PortfolioUpdate, PortfolioOut
from app.models.portfolio_model import Portfolio as PortfolioModel
from app.models.user_model import User as UserModel


class PortfolioController:
    @staticmethod
    def create_portfolio(db: Session, portfolio: PortfolioCreate) -> PortfolioOut:
        # Check if the user exists
        db_user = db.query(UserModel).filter(UserModel.id == portfolio.user_id).first()

        if db_user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )

        new_portfolio = PortfolioModel(
            name=portfolio.name,
            description=portfolio.description,
            user_id=portfolio.user_id,
        )

        db.add(new_portfolio)
        try:
            db.commit()
            db.refresh(new_portfolio)
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Portfolio already exists",
            )

        portfolio_out = PortfolioOut.model_validate(new_portfolio)

        return portfolio_out

    @staticmethod
    def get_portfolio_by_id(db: Session, portfolio_id: int) -> None | PortfolioOut:
        return (
            db.query(PortfolioModel).filter(PortfolioModel.id == portfolio_id).first()
        )

    @staticmethod
    def get_portfolios(
        db: Session, skip: int = 0, limit: int = 10
    ) -> list[PortfolioOut]:
        return db.query(PortfolioModel).offset(skip).limit(limit).all()

    @staticmethod
    def update_portfolio_by_id(
        db: Session, portfolio_id: int, portfolio: PortfolioUpdate
    ) -> None | PortfolioOut:
        db_portfolio = (
            db.query(PortfolioModel).filter(PortfolioModel.id == portfolio_id).first()
        )

        if db_portfolio is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Portfolio not found"
            )

        # Update the portfolio attributes
        if portfolio.name:
            db_portfolio.name = portfolio.name
        if portfolio.description:
            db_portfolio.description = portfolio.description

        try:
            db.commit()
            db.refresh(db_portfolio)
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Portfolio update conflict",
            )

        portfolio_out = PortfolioOut.model_validate(db_portfolio)

        return portfolio_out

    @staticmethod
    def delete_portfolio_by_id(db: Session, portfolio_id: int) -> None | str:
        db.query(PortfolioModel).filter(PortfolioModel.id == portfolio_id).delete()
        db.commit()
        return "Portfolio deleted successfully"
