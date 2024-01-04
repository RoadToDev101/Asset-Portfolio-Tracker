from typing import Tuple, List
from sqlalchemy import ClauseElement
from app.utils.custom_exceptions import BadRequestException, NotFoundException
from app.utils.common_utils import remove_private_attributes
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from psycopg2.errors import UniqueViolation
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

        new_transaction = TransactionModel(
            transaction_type=transaction.transaction_type,
            coin_symbol=transaction.coin_symbol,
            user_id=transaction.user_id,
            amount=transaction.amount,
            price_per_token=transaction.price_per_token,
            portfolio_id=transaction.portfolio_id,
        )

        db.add(new_transaction)

        try:
            db.commit()
            db.refresh(new_transaction)
        except IntegrityError as e:
            db.rollback()
            if isinstance(e.orig, UniqueViolation):
                raise BadRequestException("Transaction already exists")
            else:
                raise BadRequestException(f"Failed to create transaction: {e.orig}")

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
    ) -> Tuple[List[TransactionOut], int]:
        return TransactionController._get_transactions(
            db, None, skip, limit, start_time, end_time
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
        if transaction.transaction_type:
            db_transaction.transaction_type = transaction.transaction_type
        if transaction.coin_symbol:
            db_transaction.coin_symbol = transaction.coin_symbol
        if transaction.amount:
            db_transaction.amount = transaction.amount
        if transaction.price_per_token:
            db_transaction.price_per_token = transaction.price_per_token

        try:
            db.commit()
            db.refresh(db_transaction)
        except IntegrityError as e:
            db.rollback()
            if isinstance(e.orig, UniqueViolation):
                raise BadRequestException("Transaction already exists")
            else:
                raise BadRequestException(f"Failed to update transaction: {e.orig}")
        transaction_dict = remove_private_attributes(db_transaction)
        transaction_out = TransactionOut.model_validate(transaction_dict)

        return transaction_out

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
        return "Transaction deleted successfully"
