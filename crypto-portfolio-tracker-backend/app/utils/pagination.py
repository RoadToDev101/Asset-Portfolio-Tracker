from math import ceil
from typing import Type, TypeVar, Generic
from pydantic import BaseModel

DataT = TypeVar("DataT")


class PaginationMeta(BaseModel):
    page: int
    page_size: int
    total: int
    total_pages: int


class Pagination(BaseModel, Generic[DataT]):
    data: list[DataT]
    pagination: PaginationMeta

    @classmethod
    def total_pages(cls, total: int, page_size: int) -> int:
        # Calculate total pages and use ceil to round up
        return ceil(total / page_size)

    @classmethod
    def create(
        cls: Type["Pagination[DataT]"],
        data: list[DataT],
        page: int,
        page_size: int,
        total: int,
    ) -> "Pagination[DataT]":
        pagination = PaginationMeta(
            page=page,
            page_size=page_size,
            total=total,
            total_pages=cls.total_pages(total, page_size),  # Corrected call
        )
        return cls(data=data, pagination=pagination)
