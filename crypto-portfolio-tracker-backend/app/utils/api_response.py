from pydantic import BaseModel, Field
from typing import Generic, TypeVar, Optional, List

DataT = TypeVar("DataT")


class ApiResponse(BaseModel, Generic[DataT]):
    success: Optional[bool] = Field(
        None, description="Whether the request was successful or not"
    )
    message: Optional[str] = Field(None, description="A message about the result")
    data: Optional[DataT] = Field(None, description="Data payload of the response")
    errors: List[str] = Field(default_factory=list, description="List of error details")

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

    @classmethod
    def failure_response(
        cls, message: str = "Operation failed", errors: List[str] = None
    ):
        return cls(success=False, message=message, errors=errors or [])

    class ConfigDictDict:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Operation successful",
                "data": {
                    "id": "e9f7d3e0-1c1a-4e5a-8f2a-0f8a6b6f1b2d",
                    "username": "user1",
                    "email": "user1@gmail.com",
                },
                "errors": [],
            }
        }
