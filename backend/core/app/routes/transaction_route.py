from fastapi import APIRouter, Depends, status, Query
from app.dependencies import get_current_user, get_current_active_admin
from app.utils.api_response import ApiResponse
from app.schemas.user_schema import UserOut
from app.dependencies import get_db
from sqlalchemy.orm import Session
from app.controllers.transaction_controller import TransactionController
from app.controllers.portfolio_controller import PortfolioController
from app.schemas.transaction_schema import (
    TransactionOut,
    TransactionCreate,
    TransactionUpdate,
)
from app.models.transaction_model import Transaction as TransactionModel
from uuid import UUID
from app.utils.custom_exceptions import ForbiddenException
from app.utils.pagination import Pagination
from datetime import datetime


router = APIRouter(
    prefix="/api/v1/transactions",
    tags=["Transactions"],
    dependencies=[Depends(get_current_user)],
)


# Create transaction. Validate that only the owner can create a transaction
@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=ApiResponse[TransactionOut],
)
async def create_transaction(
    transaction: TransactionCreate,
    db: Session = Depends(get_db),
    current_user: UserOut = Depends(get_current_user),
):
    if current_user.id != transaction.user_id:
        raise ForbiddenException
    transaction = TransactionController.create_transaction(db, transaction)
    return ApiResponse[TransactionOut].success_response(
        data=transaction, message="Transaction created successfully"
    )


# Get all transactions created by all users (admin only)
@router.get(
    "/admin",
    status_code=status.HTTP_200_OK,
    response_model=ApiResponse[Pagination[TransactionOut]],
    dependencies=[Depends(get_current_active_admin)],
)
async def get_all_transactions_in_db(
    page: int = Query(gt=0),
    page_size: int = Query(gt=0),
    start_time: datetime = None,
    end_time: datetime = None,
    include_deleted: bool = False,
    db: Session = Depends(get_db),
):
    skip = (page - 1) * page_size
    transactions, total = TransactionController.get_all_transactions(
        db,
        skip=skip,
        limit=page_size,
        start_time=start_time,
        end_time=end_time,
        include_deleted=include_deleted,
    )

    result = Pagination[TransactionOut].create(transactions, page, page_size, total)
    return ApiResponse[Pagination[TransactionOut]].success_response(
        data=result, message="Transactions retrieved successfully"
    )


# Get all transactions created by a user
@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=ApiResponse[Pagination[TransactionOut]],
)
async def get_transactions_by_user(
    user_id: UUID,
    page: int = Query(gt=0),
    page_size: int = Query(gt=0),
    start_time: datetime = None,
    end_time: datetime = None,
    db: Session = Depends(get_db),
    current_user: UserOut = Depends(get_current_user),
):
    if current_user.id != user_id:
        raise ForbiddenException
    skip = (page - 1) * page_size
    transactions, total = TransactionController.get_transactions_by_user_id(
        db,
        user_id,
        skip=skip,
        limit=page_size,
        start_time=start_time,
        end_time=end_time,
    )

    result = Pagination[TransactionOut].create(transactions, page, page_size, total)
    return ApiResponse[Pagination[TransactionOut]].success_response(
        data=result, message="Transactions retrieved successfully"
    )


# Get transaction by id and validate that the user is the owner
@router.get(
    "/{transaction_id}",
    status_code=status.HTTP_200_OK,
    response_model=ApiResponse[TransactionOut],
)
async def get_transaction(
    transaction_id: UUID,
    db: Session = Depends(get_db),
    current_user: UserOut = Depends(get_current_user),
):
    transaction = TransactionController.get_transaction_by_id(
        db, transaction_id=transaction_id
    )
    if current_user.id != transaction.user_id:
        raise ForbiddenException
    return ApiResponse[TransactionOut].success_response(data=transaction)


# Get all transactions for a portfolio and validate that the user is the owner
@router.get(
    "/portfolio/{portfolio_id}",
    status_code=status.HTTP_200_OK,
    response_model=ApiResponse[Pagination[TransactionOut]],
)
async def get_portfolio_transactions(
    portfolio_id: UUID,
    page: int = Query(gt=0),
    page_size: int = Query(gt=0),
    start_time: datetime = None,
    end_time: datetime = None,
    db: Session = Depends(get_db),
    current_user: UserOut = Depends(get_current_user),
):
    portfolio = PortfolioController.get_portfolio_by_id(db, portfolio_id=portfolio_id)
    if current_user.id != portfolio.user_id:
        raise ForbiddenException
    skip = (page - 1) * page_size
    transactions, total = TransactionController.get_transactions_by_portfolio_id(
        db,
        portfolio_id=portfolio_id,
        skip=skip,
        limit=page_size,
        start_time=start_time,
        end_time=end_time,
    )

    result = Pagination[TransactionOut].create(transactions, page, page_size, total)
    return ApiResponse[Pagination[TransactionOut]].success_response(
        data=result, message="Transactions retrieved successfully"
    )


# Update transaction by id and validate that the user is the owner
@router.patch(
    "/{transaction_id}",
    status_code=status.HTTP_200_OK,
    response_model=ApiResponse[TransactionOut],
)
async def update_transaction(
    transaction_id: UUID,
    transaction: TransactionUpdate,
    db: Session = Depends(get_db),
    current_user: UserOut = Depends(get_current_user),
):
    transaction = TransactionController.update_transaction_by_id(
        db, transaction_id=transaction_id, transaction=transaction
    )
    if current_user.id != transaction.user_id:
        raise ForbiddenException
    return ApiResponse[TransactionOut].success_response(
        data=transaction, message="Transaction updated successfully"
    )


# Delete transaction by id and validate that the user is the owner
@router.delete(
    "/{transaction_id}",
    status_code=status.HTTP_200_OK,
    response_model=ApiResponse[str],
)
async def delete_transaction(
    transaction_id: UUID,
    db: Session = Depends(get_db),
    current_user: UserOut = Depends(get_current_user),
):
    transaction = TransactionController.get_transaction_by_id(
        db, transaction_id=transaction_id
    )
    if current_user.id != transaction.user_id:
        raise ForbiddenException
    message = TransactionController.soft_delete_transaction_by_id(
        db, transaction_id=transaction_id
    )
    return ApiResponse[str].success_response(message=message)


# Hard delete transaction by id (admin only)
@router.delete(
    "/admin/{transaction_id}",
    status_code=status.HTTP_200_OK,
    response_model=ApiResponse[str],
    dependencies=[Depends(get_current_active_admin)],
)
async def hard_delete_transaction(transaction_id: UUID, db: Session = Depends(get_db)):
    message = TransactionController.hard_delete_transaction_by_id(
        db, transaction_id=transaction_id
    )
    return ApiResponse[str].success_response(message=message)
