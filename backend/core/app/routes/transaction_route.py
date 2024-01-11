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
    """
    Create a new transaction.

    Args:
        transaction (TransactionCreate): The transaction data.
        db (Session, optional): The database session. Defaults to Depends(get_db).
        current_user (UserOut, optional): The current user. Defaults to Depends(get_current_user).

    Raises:
        ForbiddenException: If the current user is not authorized to create the transaction.

    Returns:
        ApiResponse[TransactionOut]: The API response containing the created transaction.
    """
    if current_user.id != transaction.user_id:
        raise ForbiddenException
    transaction = TransactionController.create_transaction(db, transaction)
    return ApiResponse[TransactionOut].success_response(
        data=transaction, message="Transaction created successfully"
    )


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
    """
    Retrieve all transactions from the database. This is an admin only endpoint.

    Args:
        page (int): The page number for pagination (default: 1).
        page_size (int): The number of transactions per page (default: 10).
        start_time (datetime): The start time to filter transactions (optional).
        end_time (datetime): The end time to filter transactions (optional).
        include_deleted (bool): Flag to include deleted transactions (default: False).
        db (Session): The database session.

    Returns:
        ApiResponse[Pagination[TransactionOut]]: The API response containing the paginated transactions.

    Raises:
        None.
    """
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
    """
    Retrieve transactions for a specific user.

    Args:
        user_id (UUID): The ID of the user.
        page (int, optional): The page number. Defaults to 1.
        page_size (int, optional): The number of transactions per page. Defaults to 10.
        start_time (datetime, optional): The start time of the transactions. Defaults to None.
        end_time (datetime, optional): The end time of the transactions. Defaults to None.
        db (Session, optional): The database session. Defaults to Depends(get_db).
        current_user (UserOut, optional): The current authenticated user. Defaults to Depends(get_current_user).

    Returns:
        ApiResponse[Pagination[TransactionOut]]: The API response containing the paginated transactions.
    """
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
    """
    Retrieve a transaction by its ID. This endpoint is only accessible by the owner of the transaction.

    Args:
        transaction_id (UUID): The ID of the transaction to retrieve.
        db (Session, optional): The database session. Defaults to Depends(get_db).
        current_user (UserOut, optional): The current authenticated user. Defaults to Depends(get_current_user).

    Returns:
        ApiResponse[TransactionOut]: The API response containing the retrieved transaction.
    """
    transaction = TransactionController.get_transaction_by_id(
        db, transaction_id=transaction_id
    )
    if current_user.id != transaction.user_id:
        raise ForbiddenException
    return ApiResponse[TransactionOut].success_response(data=transaction)


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
    """
    Retrieve transactions for a specific portfolio.

    Args:
        portfolio_id (UUID): The ID of the portfolio.
        page (int, optional): The page number for pagination. Defaults to 1.
        page_size (int, optional): The number of transactions per page. Defaults to 10.
        start_time (datetime, optional): The start time to filter transactions. Defaults to None.
        end_time (datetime, optional): The end time to filter transactions. Defaults to None.
        db (Session, optional): The database session. Defaults to Depends(get_db).
        current_user (UserOut, optional): The current authenticated user. Defaults to Depends(get_current_user).

    Returns:
        ApiResponse[Pagination[TransactionOut]]: The API response containing the paginated transactions.

    Raises:
        ForbiddenException: If the current user does not have access to the portfolio.
    """
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
    """
    Update a transaction by its ID. This endpoint is only accessible by the owner of the transaction.

    Args:
        transaction_id (UUID): The ID of the transaction to be updated.
        transaction (TransactionUpdate): The updated transaction data.
        db (Session, optional): The database session. Defaults to Depends(get_db).
        current_user (UserOut, optional): The current authenticated user. Defaults to Depends(get_current_user).

    Returns:
        ApiResponse[TransactionOut]: The API response containing the updated transaction data.
    """
    transaction = TransactionController.update_transaction_by_id(
        db, transaction_id=transaction_id, transaction=transaction
    )
    if current_user.id != transaction.user_id:
        raise ForbiddenException
    return ApiResponse[TransactionOut].success_response(
        data=transaction, message="Transaction updated successfully"
    )


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
    """
    Soft delete a transaction by its ID. This endpoint is only accessible by the owner of the transaction.

    Args:
        transaction_id (UUID): The ID of the transaction to be deleted.
        db (Session, optional): The database session. Defaults to Depends(get_db).
        current_user (UserOut, optional): The current authenticated user. Defaults to Depends(get_current_user).

    Raises:
        ForbiddenException: If the current user is not the owner of the transaction.

    Returns:
        ApiResponse[str]: The API response indicating the success of the deletion.
    """
    transaction = TransactionController.get_transaction_by_id(
        db, transaction_id=transaction_id
    )
    if current_user.id != transaction.user_id:
        raise ForbiddenException
    message = TransactionController.soft_delete_transaction_by_id(
        db, transaction_id=transaction_id
    )
    return ApiResponse[str].success_response(message=message)


@router.delete(
    "/admin/{transaction_id}",
    status_code=status.HTTP_200_OK,
    response_model=ApiResponse[str],
    dependencies=[Depends(get_current_active_admin)],
)
async def hard_delete_transaction(transaction_id: UUID, db: Session = Depends(get_db)):
    """
    Hard delete a transaction by its ID from the database. This is an admin only endpoint.

    Args:
        transaction_id (UUID): The ID of the transaction to be deleted.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        ApiResponse[str]: The API response indicating the success or failure of the deletion.
    """
    message = TransactionController.hard_delete_transaction_by_id(
        db, transaction_id=transaction_id
    )
    return ApiResponse[str].success_response(message=message)
