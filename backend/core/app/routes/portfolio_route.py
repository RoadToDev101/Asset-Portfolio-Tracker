from fastapi import APIRouter, Depends, status, Query
from app.dependencies import get_current_user, get_current_active_admin
from app.schemas.api_response import ApiResponse
from app.schemas.pagination import Pagination
from app.schemas.portfolio_schema import PortfolioOut, PortfolioCreate, PortfolioUpdate
from app.schemas.user_schema import UserOut
from app.dependencies import get_db
from sqlalchemy.orm import Session
from app.controllers.portfolio_controller import PortfolioController
from app.models.portfolio_model import Portfolio as PortfolioModel
from uuid import UUID
from app.utils.custom_exceptions import ForbiddenException


router = APIRouter(
    prefix="/api/v1/portfolios",
    tags=["Portfolios"],
    dependencies=[Depends(get_current_user)],
)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=ApiResponse[PortfolioOut],
)
async def create_portfolio(
    portfolio: PortfolioCreate,
    db: Session = Depends(get_db),
    current_user: UserOut = Depends(get_current_user),
):
    """
    Create a new portfolio for the current user.

    Args:
        portfolio (PortfolioCreate): The portfolio data to be created.
        db (Session, optional): The database session. Defaults to Depends(get_db).
        current_user (UserOut, optional): The current authenticated user. Defaults to Depends(get_current_user).

    Raises:
        ForbiddenException: If the current user is not the owner of the portfolio.

    Returns:
        ApiResponse[PortfolioOut]: The API response containing the created portfolio.
    """
    if current_user.id != portfolio.user_id:
        raise ForbiddenException
    portfolio = PortfolioController.create_portfolio(db, portfolio)
    return ApiResponse[PortfolioOut].success_response(
        data=portfolio, message="Portfolio created successfully"
    )


@router.get(
    "/admin",
    status_code=status.HTTP_200_OK,
    response_model=ApiResponse[Pagination[PortfolioOut]],
    dependencies=[Depends(get_current_active_admin)],
)
async def get_all_portfolios_in_db(
    page: int = Query(gt=0),
    page_size: int = Query(gt=0),
    db: Session = Depends(get_db),
):
    """
    Retrieve all portfolios from the database.

    Args:
        page (int): The page number of the results (default: 1).
        page_size (int): The number of portfolios per page (default: 10).
        db (Session): The database session.

    Returns:
        ApiResponse[Pagination[PortfolioOut]]: The API response containing the paginated portfolios.

    Raises:
        None.
    """
    skip = (page - 1) * page_size
    portfolios = PortfolioController.get_all_portfolios(db, skip=skip, limit=page_size)
    total = db.query(PortfolioModel).count()
    result = Pagination[PortfolioOut].create(portfolios, page, page_size, total)
    return ApiResponse[Pagination[PortfolioOut]].success_response(
        data=result, message="Portfolios retrieved successfully"
    )


@router.get(
    "/{portfolio_id}",
    status_code=status.HTTP_200_OK,
    response_model=ApiResponse[PortfolioOut],
)
async def get_portfolio(
    portfolio_id: UUID,
    db: Session = Depends(get_db),
    current_user: UserOut = Depends(get_current_user),
):
    """
    Retrieve a portfolio by its ID.

    Args:
        portfolio_id (UUID): The ID of the portfolio to retrieve.
        db (Session, optional): The database session. Defaults to Depends(get_db).
        current_user (UserOut, optional): The current authenticated user. Defaults to Depends(get_current_user).

    Returns:
        ApiResponse[PortfolioOut]: The API response containing the retrieved portfolio.
    """
    portfolio = PortfolioController.get_portfolio_by_id(db, portfolio_id=portfolio_id)
    if current_user.id != portfolio.user_id:
        raise ForbiddenException
    return ApiResponse[PortfolioOut].success_response(data=portfolio)


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=ApiResponse[Pagination[PortfolioOut]],
)
async def get_user_portfolios(
    page: int = Query(gt=0),
    page_size: int = Query(gt=0),
    db: Session = Depends(get_db),
    current_user: UserOut = Depends(get_current_user),
):
    """
    Retrieve the portfolios of the current user.

    Args:
        page (int): The page number of the results to retrieve.
        page_size (int): The number of results per page.
        db (Session): The database session.
        current_user (UserOut): The current authenticated user.

    Returns:
        ApiResponse[Pagination[PortfolioOut]]: The API response containing the paginated portfolios.
    """
    skip = (page - 1) * page_size
    portfolios = PortfolioController.get_portfolios_by_user_id(
        db, user_id=current_user.id, skip=skip, limit=page_size
    )
    total = (
        db.query(PortfolioModel)
        .filter(PortfolioModel.user_id == current_user.id)
        .count()
    )
    result = Pagination[PortfolioOut].create(portfolios, page, page_size, total)
    return ApiResponse[Pagination[PortfolioOut]].success_response(
        data=result, message="Portfolios retrieved successfully"
    )


@router.patch(
    "/{portfolio_id}",
    status_code=status.HTTP_200_OK,
    response_model=ApiResponse[PortfolioOut],
)
async def update_portfolio(
    portfolio_id: UUID,
    portfolio: PortfolioUpdate,
    db: Session = Depends(get_db),
    current_user: UserOut = Depends(get_current_user),
):
    """
    Update a portfolio by its ID.

    Args:
        portfolio_id (UUID): The ID of the portfolio to be updated.
        portfolio (PortfolioUpdate): The updated portfolio data.
        db (Session, optional): The database session. Defaults to Depends(get_db).
        current_user (UserOut, optional): The current authenticated user. Defaults to Depends(get_current_user).

    Returns:
        ApiResponse[PortfolioOut]: The API response containing the updated portfolio data.

    Raises:
        ForbiddenException: If the current user is not the owner of the portfolio.
    """
    portfolio = PortfolioController.update_portfolio_by_id(
        db, portfolio_id=portfolio_id, portfolio=portfolio
    )
    if current_user.id != portfolio.user_id:
        raise ForbiddenException
    return ApiResponse[PortfolioOut].success_response(
        data=portfolio, message="Portfolio updated successfully"
    )


@router.delete(
    "/{portfolio_id}",
    status_code=status.HTTP_200_OK,
    response_model=ApiResponse[str],
)
async def delete_portfolio(
    portfolio_id: UUID,
    db: Session = Depends(get_db),
    current_user: UserOut = Depends(get_current_user),
):
    """
    Delete a portfolio by its ID.

    Args:
        portfolio_id (UUID): The ID of the portfolio to be deleted.
        db (Session, optional): The database session. Defaults to Depends(get_db).
        current_user (UserOut, optional): The current authenticated user. Defaults to Depends(get_current_user).

    Returns:
        ApiResponse[str]: The API response indicating the success message of the operation.
    """
    portfolio = PortfolioController.get_portfolio_by_id(db, portfolio_id=portfolio_id)
    if current_user.id != portfolio.user_id:
        raise ForbiddenException
    mmessage = PortfolioController.delete_portfolio_by_id(db, portfolio_id=portfolio_id)
    return ApiResponse[str].success_response(message=mmessage)
