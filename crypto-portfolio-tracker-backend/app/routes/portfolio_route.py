from fastapi import APIRouter, Depends, status, Query
from app.dependencies import get_current_user, get_current_active_admin
from app.utils.api_response import ApiResponse
from app.utils.pagination import Pagination
from app.schemas.portfolio_schema import PortfolioOut, PortfolioCreate
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


# Create portfolio. Validate that only the owner can create a portfolio
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
    if current_user.id != portfolio.user_id:
        raise ForbiddenException
    portfolio = PortfolioController.create_portfolio(db, portfolio)
    return ApiResponse[PortfolioOut].success_response(
        data=portfolio, message="Portfolio created successfully"
    )


# Get all portfolios created by all users (admin only)
@router.get(
    "/all",
    status_code=status.HTTP_200_OK,
    response_model=ApiResponse[Pagination[PortfolioOut]],
    dependencies=[Depends(get_current_active_admin)],
)
async def get_all_portfolios(
    page: int = Query(gt=0),
    page_size: int = Query(gt=0),
    db: Session = Depends(get_db),
):
    skip = (page - 1) * page_size
    portfolios = PortfolioController.get_all_portfolios(db, skip=skip, limit=page_size)
    total = db.query(PortfolioModel).count()
    result = Pagination[PortfolioOut].create(portfolios, page, page_size, total)
    return ApiResponse[Pagination[PortfolioOut]].success_response(
        data=result, message="Portfolios retrieved successfully"
    )


# Get portfoloio by id and validate that the user is the owner
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
    portfolio = PortfolioController.get_portfolio_by_id(db, portfolio_id=portfolio_id)
    if current_user.id != portfolio.user_id:
        raise ForbiddenException
    return ApiResponse[PortfolioOut].success_response(data=portfolio)


# Get all portfolios for a user
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
