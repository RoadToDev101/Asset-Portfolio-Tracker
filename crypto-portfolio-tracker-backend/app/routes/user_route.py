from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.controllers.user_controller import UserController
from app.schemas.user_schema import UserUpdate, UserOut
from app.models.user_model import User as UserModel
from app.utils.pagination import Pagination
from app.dependencies import get_current_user, get_current_active_admin
from uuid import UUID
from app.utils.api_response import ApiResponse

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
    if current_user.role != "admin" and current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions"
        )
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
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions"
        )

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
):
    message = UserController.delete_user_by_id(db, user_id=user_id)
    return ApiResponse[str].with_message(message=message)
