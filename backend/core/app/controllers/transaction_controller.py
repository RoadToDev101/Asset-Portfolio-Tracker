from typing import Tuple, List
from sqlalchemy import ClauseElement, or_
from app.utils.custom_exceptions import BadRequestException, NotFoundException
from app.utils.common_utils import remove_private_attributes
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.schemas.transaction_schema import (
    TransactionCreate,
    TransactionOut,
    TransactionUpdate,
)
from app.models.transaction_model import Transaction as TransactionModel
from app.models.user_model import User as UserModel
from app.models.portfolio_model import Portfolio as PortfolioModel
from datetime import datetime


class TransactionController:
    @staticmethod
    def create_transaction(
        db: Session, transaction: TransactionCreate
    ) -> TransactionOut:
        # Check if the user exists
        db_user = db.query(UserModel).get(transaction.user_id)

        if db_user is None:
            raise NotFoundException("User not found")

        # Check if the portfolio exists
        db_portfolio = db.query(PortfolioModel).get(transaction.portfolio_id)

        if db_portfolio is None:
            raise NotFoundException("Portfolio not found")

        # Check if the transaction asset type is valid
        if transaction.asset_type != db_portfolio.asset_type:
            raise BadRequestException(
                "Transaction asset type does not match portfolio asset type"
            )

        new_transaction = TransactionModel(
            description=transaction.description,
            transaction_type=transaction.transaction_type,
            asset_type=transaction.asset_type,
            ticker=transaction.ticker,
            user_id=transaction.user_id,
            amount=transaction.amount,
            currency=transaction.currency,
            unit_price=transaction.unit_price,
            transaction_fee=transaction.transaction_fee,
            portfolio_id=transaction.portfolio_id,
        )

        db.add(new_transaction)

        try:
            db.commit()
            db.refresh(new_transaction)
        except SQLAlchemyError:
            db.rollback()
            raise BadRequestException("Failed to create transaction")

        transaction_dict = remove_private_attributes(new_transaction)
        transaction_out = TransactionOut.model_validate(transaction_dict)

        return transaction_out

    @staticmethod
    def get_transaction_by_id(db: Session, transaction_id: UUID) -> TransactionOut:
        transaction = db.query(TransactionModel).get(transaction_id)
        if transaction is None:
            raise NotFoundException("Transaction not found")
        transaction_dict = remove_private_attributes(transaction)
        transaction_out = TransactionOut.model_validate(transaction_dict)
        return transaction_out

    @staticmethod
    def _get_transactions(
        db: Session,
        filter_condition: ClauseElement = None,
        skip: int = 0,
        limit: int = 10,
        start_time: datetime = None,
        end_time: datetime = None,
        include_deleted: bool = False,
    ) -> Tuple[List[TransactionOut], int]:
        try:
            query = db.query(TransactionModel)

            if filter_condition:
                query = query.filter(filter_condition)

            if start_time and end_time:
                query = query.filter(
                    TransactionModel.created_at.between(start_time, end_time)
                )

            if start_time and not end_time:
                query = query.filter(TransactionModel.created_at >= start_time)

            if end_time and not start_time:
                query = query.filter(TransactionModel.created_at <= end_time)

            if not include_deleted:
                query = query.filter(
                    or_(
                        TransactionModel.deleted_at.is_(None),
                        TransactionModel.deleted_at > datetime.utcnow(),
                    )
                )

            total = query.count()
            transactions = query.offset(skip).limit(limit).all()
            results = []
            for transaction in transactions:
                transaction_dict = remove_private_attributes(transaction)
                transaction_out = TransactionOut.model_validate(transaction_dict)
                results.append(transaction_out)
            return results, total
        except SQLAlchemyError:
            raise BadRequestException("Failed to retrieve transactions")

    @staticmethod
    def get_all_transactions(
        db: Session,
        skip: int = 0,
        limit: int = 10,
        start_time: datetime = None,
        end_time: datetime = None,
        include_deleted: bool = False,
    ) -> Tuple[List[TransactionOut], int]:
        return TransactionController._get_transactions(
            db, None, skip, limit, start_time, end_time, include_deleted
        )

    @staticmethod
    def get_transactions_by_user_id(
        db: Session,
        user_id: UUID,
        skip: int = 0,
        limit: int = 10,
        start_time: datetime = None,
        end_time: datetime = None,
    ) -> Tuple[List[TransactionOut], int]:
        return TransactionController._get_transactions(
            db, TransactionModel.user_id == user_id, skip, limit, start_time, end_time
        )

    @staticmethod
    def get_transactions_by_portfolio_id(
        db: Session,
        portfolio_id: UUID,
        skip: int = 0,
        limit: int = 10,
        start_time: datetime = None,
        end_time: datetime = None,
    ) -> Tuple[List[TransactionOut], int]:
        return TransactionController._get_transactions(
            db,
            TransactionModel.portfolio_id == portfolio_id,
            skip,
            limit,
            start_time,
            end_time,
        )

    @staticmethod
    def update_transaction_by_id(
        db: Session, transaction_id: UUID, transaction: TransactionUpdate
    ) -> TransactionOut:
        db_transaction = db.query(TransactionModel).get(transaction_id)

        if db_transaction is None:
            raise NotFoundException("Transaction not found")

        # Update the transaction attributes
        if transaction.description:
            db_transaction.description = transaction.description
        if transaction.transaction_type:
            db_transaction.transaction_type = transaction.transaction_type
        if transaction.ticker:
            db_transaction.ticker = transaction.ticker
        if transaction.amount:
            db_transaction.amount = transaction.amount
        if transaction.currency:
            db_transaction.currency = transaction.currency
        if transaction.unit_price:
            db_transaction.unit_price = transaction.unit_price
        if transaction.transaction_fee:
            db_transaction.transaction_fee = transaction.transaction_fee

        try:
            db.commit()
            db.refresh(db_transaction)
        except SQLAlchemyError:
            db.rollback()
            raise BadRequestException("Failed to update transaction")

        transaction_dict = remove_private_attributes(db_transaction)
        transaction_out = TransactionOut.model_validate(transaction_dict)

        return transaction_out

    @staticmethod
    def soft_delete_transaction_by_id(db: Session, transaction_id: UUID) -> str:
        transaction = db.query(TransactionModel).get(transaction_id)
        if transaction is None:
            raise NotFoundException("Transaction not found")

        transaction.deleted_at = datetime.utcnow()

        try:
            db.commit()
        except SQLAlchemyError:
            db.rollback()
            raise BadRequestException("Failed to delete transaction")
        return "Transaction deleted successfully"

    @staticmethod
    def delete_transaction_by_id(db: Session, transaction_id: UUID) -> str:
        transaction = db.query(TransactionModel).get(transaction_id)
        if transaction is None:
            raise NotFoundException("Transaction not found")

        db.delete(transaction)

        try:
            db.commit()
        except SQLAlchemyError:
            db.rollback()
            raise BadRequestException("Failed to delete transaction")
        return "Transaction hard deleted successfully"
