from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.controllers.user_controller import UserController
from app.schemas.user_schema import UserUpdate, UserOut
from app.models.user_model import User as UserModel
from app.schemas.pagination import Pagination
from app.dependencies import get_current_user, get_current_active_admin
from uuid import UUID
from app.schemas.api_response import ApiResponse
from app.utils.custom_exceptions import ForbiddenException

router = APIRouter(
    prefix="/api/v1/users", tags=["Users"], dependencies=[Depends(get_current_user)]
)


@router.get(
    "/{user_id}", status_code=status.HTTP_200_OK, response_model=ApiResponse[UserOut]
)
async def get_user(
    user_id: UUID,
    db: Session = Depends(get_db),
    current_user: UserOut = Depends(get_current_user),
):
    """
    Retrieve a user by their ID.

    Args:
        user_id (UUID): The ID of the user to retrieve.
        db (Session, optional): The database session. Defaults to Depends(get_db).
        current_user (UserOut, optional): The current authenticated user. Defaults to Depends(get_current_user).

    Raises:
        ForbiddenException: If the current user is not an admin and not the same as the requested user.

    Returns:
        ApiResponse[UserOut]: The API response containing the user data.
    """
    if current_user.role != "admin" and current_user.id != user_id:
        raise ForbiddenException
    user = UserController.get_user_by_id(db, user_id=user_id)
    return ApiResponse[UserOut].success_response(data=user)


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=ApiResponse[Pagination[UserOut]],
    dependencies=[Depends(get_current_active_admin)],
)
async def get_all_users(
    page: int = Query(gt=0),
    page_size: int = Query(gt=0),
    db: Session = Depends(get_db),
):
    """
    Retrieve all users with pagination.

    Args:
        page (int): The page number to retrieve (default: 1).
        page_size (int): The number of users per page (default: 10).
        db (Session): The database session.

    Returns:
        ApiResponse[Pagination[UserOut]]: The API response containing the paginated users.
    """
    skip = (page - 1) * page_size
    users = UserController.get_users(db, skip=skip, limit=page_size)
    total = db.query(UserModel).count()
    result = Pagination[UserOut].create(users, page, page_size, total)
    return ApiResponse[Pagination[UserOut]].success_response(
        data=result, message="Users retrieved successfully"
    )


@router.patch(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
    response_model=ApiResponse[UserOut],
)
async def update_user(
    user_id: UUID,
    user: UserUpdate,
    db: Session = Depends(get_db),
    current_user: UserOut = Depends(get_current_user),
):
    """
    Update a user by their ID.

    Args:
        user_id (UUID): The ID of the user to update.
        user (UserUpdate): The updated user data.
        db (Session, optional): The database session. Defaults to Depends(get_db).
        current_user (UserOut, optional): The current authenticated user. Defaults to Depends(get_current_user).

    Raises:
        ForbiddenException: If the current user is not authorized to update the user.

    Returns:
        ApiResponse[UserOut]: The API response containing the updated user data.
    """
    if current_user.id != user_id:
        raise ForbiddenException

    update_user = UserController.update_user_by_id(db, user_id=user_id, user=user)

    return ApiResponse[UserOut].success_response(
        data=update_user, message="User updated successfully"
    )


@router.delete(
    "/{user_id}", status_code=status.HTTP_200_OK, response_model=ApiResponse[str]
)
async def delete_user(
    user_id: UUID,
    db: Session = Depends(get_db),
    current_user: UserOut = Depends(get_current_user),
):
    """
    Delete a user by their ID.

    Parameters:
    - user_id (UUID): The ID of the user to be deleted.
    - db (Session, optional): The database session. Defaults to Depends(get_db).
    - current_user (UserOut, optional): The current authenticated user. Defaults to Depends(get_current_user).

    Returns:
    - ApiResponse[str]: The API response indicating the success or failure of the operation.
    """
    if current_user.id != user_id and current_user.role != "admin":
        raise ForbiddenException
    message = UserController.delete_user_by_id(db, user_id=user_id)
    return ApiResponse[str].success_response(message=message)
