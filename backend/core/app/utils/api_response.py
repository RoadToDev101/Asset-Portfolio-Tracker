from pydantic import BaseModel, Field
from typing import Generic, TypeVar, Optional
from uuid import UUID

DataT = TypeVar("DataT")


class ApiResponse(BaseModel, Generic[DataT]):
    success: Optional[bool] = Field(
        None, description="Whether the request was successful or not"
    )
    message: Optional[str] = Field(None, description="A message about the result")
    data: Optional[DataT] = Field(None, description="Data payload of the response")

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


# class TokenResponse(ApiResponse[DataT]):
#     access_token: Optional[str] = Field(None, description="Access token for the user")
#     token_type: Optional[str] = Field(None, description="Type of the access token")
#     user_id: Optional[UUID] = Field(
#         None, description="User ID of the authenticated user"
#     )

#     @classmethod
#     def token_response(
#         cls,
#         message: str = "Authentication successful",
#         data: Optional[DataT] = None,
#         access_token: str = None,
#         token_type: str = None,
#         user_id: UUID = None,
#     ):
#         return cls(
#             success=True,
#             message=message,
#             data=data,
#             access_token=access_token,
#             token_type=token_type,
#             user_id=user_id,
#         )

#     class ConfigDict:
#         json_schema_extra = {
#             "example": {
#                 "success": True,
#                 "message": "Authentication successful",
#                 "data": None,
#                 "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9",
#                 "token_type": "bearer",
#                 "user_id": "e9f7d3e0-1c1a-4e5a-8f2a-0f8a6b6f1b2d",
#             }
#         }
