from pydantic import BaseModel, Field
from typing import Generic, TypeVar, Optional
from uuid import UUID
from app.models.user_model import UserRole

DataT = TypeVar("DataT")


class ApiResponse(BaseModel, Generic[DataT]):
    success: Optional[bool] = Field(
        description="Whether the request was successful or not"
    )
    message: Optional[str] = Field(description="A message about the result")
    data: Optional[DataT] = Field(description="Data payload of the response")

    @classmethod
    def with_message(cls, message: str, success: Optional[bool] = None):
        return cls(success=success, message=message)

    @classmethod
    def with_data(
        cls, data: DataT, message: Optional[str] = None, success: Optional[bool] = None
    ):
        return cls(success=success, message=message, data=data)

    @classmethod
    def success_response(
        cls,
        message: str = "Operation successful",
        data: Optional[DataT] = None,
    ):
        return cls(success=True, message=message, data=data)

    class ConfigDict:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Operation successful",
                "data": {
                    "id": "e9f7d3e0-1c1a-4e5a-8f2a-0f8a6b6f1b2d",
                    "username": "user1",
                    "email": "user1@gmail.com",
                },
            }
        }


class TokenResponse(ApiResponse[DataT]):
    access_token: Optional[str] = Field(None, description="Access token for the user")
    token_type: Optional[str] = Field(None, description="Type of the access token")
    user_id: Optional[UUID] = Field(
        None, description="User ID of the authenticated user"
    )
    role: Optional[UserRole] = Field(None, description="Role of the authenticated user")
    is_active: Optional[bool] = Field(
        None, description="Whether the authenticated user is active or not"
    )

    @classmethod
    def token_response(
        cls,
        message: str = "Authentication successful",
        data: Optional[DataT] = None,
        access_token: str = None,
        token_type: str = None,
        user_id: UUID = None,
        role: UserRole = None,
        is_active: bool = None,
    ):
        return cls(
            success=True,
            message=message,
            data=data,
            access_token=access_token,
            token_type=token_type,
            user_id=user_id,
            role=role,
            is_active=is_active,
        )

    class ConfigDict:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Authentication successful",
                "data": None,
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9",
                "token_type": "bearer",
                "user_id": "e9f7d3e0-1c1a-4e5a-8f2a-0f8a6b6f1b2d",
                "role": "USER",
                "is_active": True,
            }
        }
