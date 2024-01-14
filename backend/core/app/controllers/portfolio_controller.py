from typing import List
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from psycopg2.errors import UniqueViolation
from collections import defaultdict
from app.schemas.portfolio_schema import (
    PortfolioCreate,
    PortfolioUpdate,
    PortfolioOut,
    Asset,
)
from app.models.portfolio_model import Portfolio as PortfolioModel, AssetType
from app.models.user_model import User as UserModel
from app.utils.convert import remove_private_attributes
from uuid import UUID
from app.utils.custom_exceptions import NotFoundException, BadRequestException
from .transaction_controller import TransactionController
from app.models.transaction_model import TransactionType
from app.utils.fetch_price import fetch_crypto_price


def calculate_portfolio_value(db, portfolio_id) -> float:
    transactions = TransactionController.get_transactions_by_portfolio_id(
        db, portfolio_id, include_deleted=False
    )

    if len(transactions[0]) == 0:
        return 0

    total_value = 0
    for transaction in transactions[0]:
        asset_current_market_price = (
            TransactionController.get_transaction_current_value(transaction)
        )
        if (
            transaction.transaction_type == TransactionType.BUY
            or transaction.transaction_type == TransactionType.TRANSFER_IN
        ):
            total_value += transaction.amount * asset_current_market_price
        elif (
            transaction.transaction_type == TransactionType.SELL
            or transaction.transaction_type == TransactionType.TRANSFER_OUT
        ):
            total_value -= transaction.amount * asset_current_market_price
        else:
            raise BadRequestException("Invalid transaction type")

    return total_value


# List the asset in the portfolio and their current value
def get_portfolio_assets(db, portfolio_id) -> List[Asset]:
    transactions = TransactionController.get_transactions_by_portfolio_id(
        db, portfolio_id
    )

    if len(transactions[0]) == 0:
        return []

    # Create a dictionary to hold the aggregated data for each asset
    assets = defaultdict(lambda: {"quantity": 0, "ticker_symbol": "", "asset_type": ""})

    for transaction in transactions[0]:
        asset_name = transaction.asset_name

        assets[asset_name]["ticker_symbol"] = transaction.ticker_symbol
        assets[asset_name]["asset_type"] = transaction.asset_type

        if transaction.transaction_type in [
            TransactionType.BUY,
            TransactionType.TRANSFER_IN,
        ]:
            assets[asset_name]["quantity"] += transaction.amount
        elif transaction.transaction_type in [
            TransactionType.SELL,
            TransactionType.TRANSFER_OUT,
        ]:
            assets[asset_name]["quantity"] -= transaction.amount

    # Convert the assets dictionary to a list of Asset objects
    asset_objects = []
    for asset_name, asset_data in assets.items():
        if asset_data["asset_type"] == AssetType.STOCKS:
            raise NotImplementedError("Stocks not implemented yet")
        elif asset_data["asset_type"] == AssetType.CRYPTO:
            asset_current_market_price = fetch_crypto_price(
                asset_name.lower(), transaction.currency.lower()
            )
        elif asset_data["asset_type"] == AssetType.OTHERS:
            raise NotImplementedError("Asset type not implemented yet")

        asset_objects.append(
            Asset(
                asset_name=asset_name,
                ticker_symbol=asset_data["ticker_symbol"],
                asset_type=asset_data["asset_type"],
                quantity=asset_data["quantity"],
                average_price=transaction.unit_price,
                total_value=asset_data["quantity"] * asset_current_market_price,
            )
        )

    return asset_objects


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
            asset_type=portfolio.asset_type,
        )

        db.add(new_portfolio)

        try:
            db.commit()
            db.refresh(new_portfolio)
        except IntegrityError as e:
            db.rollback()
            if isinstance(e.orig, UniqueViolation):
                raise BadRequestException("Portfolio already exists")
            else:
                raise BadRequestException(f"Failed to create portfolio: {e.orig}")

        portfolio_dict = remove_private_attributes(new_portfolio)
        portfolio_out = PortfolioOut.model_validate(portfolio_dict)

        return portfolio_out

    @staticmethod
    def get_portfolio_by_id(db: Session, portfolio_id: UUID) -> PortfolioOut:
        portfolio = db.query(PortfolioModel).get(portfolio_id)
        if portfolio is None:
            raise NotFoundException("Portfolio not found")

        portfolio.current_value = calculate_portfolio_value(db, portfolio_id)
        portfolio_dict = remove_private_attributes(portfolio)
        portfolio_out = PortfolioOut.model_validate(portfolio_dict)
        return portfolio_out

    @staticmethod
    def get_all_portfolios(
        db: Session, skip: int = 0, limit: int = 10
    ) -> List[PortfolioOut]:
        try:
            portfolios = db.query(PortfolioModel).offset(skip).limit(limit).all()
            results = []
            for portfolio in portfolios:
                portfolio.current_value = calculate_portfolio_value(db, portfolio.id)
                portfolio.assets = get_portfolio_assets(db, portfolio.id)
                portfolio_dict = remove_private_attributes(portfolio)
                portfolio_out = PortfolioOut.model_validate(portfolio_dict)
                results.append(portfolio_out)
            return results
        except SQLAlchemyError:
            raise BadRequestException("Failed to retrieve portfolios")

    @staticmethod
    def get_portfolios_by_user_id(
        db: Session, user_id: UUID, skip: int = 0, limit: int = 10
    ) -> List[PortfolioOut]:
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
                portfolio.current_value = calculate_portfolio_value(db, portfolio.id)
                portfolio.assets = get_portfolio_assets(db, portfolio.id)
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
        db_portfolio = db.query(PortfolioModel).get(portfolio_id)

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
        except SQLAlchemyError:
            db.rollback()
            raise BadRequestException("Failed to delete portfolio")

        return "Portfolio deleted successfully"
