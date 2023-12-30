from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from app.schemas.portfolio_schema import PortfolioCreate, PortfolioUpdate, PortfolioOut
from app.models.portfolio_model import Portfolio as PortfolioModel
from app.models.user_model import User as UserModel
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.portfolio_model import Portfolio as PortfolioModel
from app.utils.common_utils import remove_private_attributes
from uuid import UUID
from app.utils.custom_exceptions import NotFoundException, BadRequestException


class PortfolioController:
    @staticmethod
    def create_portfolio(db: Session, portfolio: PortfolioCreate) -> PortfolioOut:
        # Check if the user exists
        db_user = db.query(UserModel).get(portfolio.user_id)

        if db_user is None:
            raise NotFoundException("User not found")

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
            raise BadRequestException("Portfolio already exists")

        portfolio_dict = remove_private_attributes(new_portfolio)
        portfolio_out = PortfolioOut.model_validate(portfolio_dict)

        return portfolio_out

    @staticmethod
    def get_portfolio_by_id(db: Session, portfolio_id: UUID) -> PortfolioOut:
        portfolio = db.query(PortfolioModel).get(portfolio_id)
        if portfolio is None:
            raise NotFoundException("Portfolio not found")
        portfolio_dict = remove_private_attributes(portfolio)
        portfolio_out = PortfolioOut.model_validate(portfolio_dict)
        return portfolio_out

    @staticmethod
    def get_all_portfolios(
        db: Session, skip: int = 0, limit: int = 10
    ) -> list[PortfolioOut]:
        try:
            portfolios = db.query(PortfolioModel).offset(skip).limit(limit).all()
            results = []
            for portfolio in portfolios:
                portfolio_dict = remove_private_attributes(portfolio)
                portfolio_out = PortfolioOut.model_validate(portfolio_dict)
                results.append(portfolio_out)
            return results
        except SQLAlchemyError:
            raise BadRequestException("Failed to retrieve portfolios")

    @staticmethod
    def get_portfolios_by_user_id(
        db: Session, user_id: UUID, skip: int = 0, limit: int = 10
    ) -> list[PortfolioOut]:
        try:
            portfolios = (
                db.query(PortfolioModel)
                .filter(PortfolioModel.user_id == user_id)
                .offset(skip)
                .limit(limit)
                .all()
            )
            results = []
            for portfolio in portfolios:
                portfolio_dict = remove_private_attributes(portfolio)
                portfolio_out = PortfolioOut.model_validate(portfolio_dict)
                results.append(portfolio_out)
            return results
        except SQLAlchemyError:
            raise BadRequestException("Failed to retrieve portfolios")

    @staticmethod
    def update_portfolio_by_id(
        db: Session, portfolio_id: UUID, portfolio: PortfolioUpdate
    ) -> PortfolioOut:
        db_portfolio = (
            db.query(PortfolioModel).filter(PortfolioModel.id == portfolio_id).first()
        )

        if db_portfolio is None:
            raise NotFoundException("Portfolio not found")

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
            raise BadRequestException("Failed to update portfolio")

        portfolio_dict = remove_private_attributes(db_portfolio)
        portfolio_out = PortfolioOut.model_validate(portfolio_dict)

        return portfolio_out

    @staticmethod
    def delete_portfolio_by_id(db: Session, portfolio_id: UUID) -> str:
        portfolio = db.query(PortfolioModel).get(portfolio_id)
        if portfolio is None:
            raise NotFoundException("Portfolio not found")
        db.delete(portfolio)
        try:
            db.commit()
        except IntegrityError:
            db.rollback()
            raise BadRequestException("Failed to delete portfolio")

        return "Portfolio deleted successfully"
