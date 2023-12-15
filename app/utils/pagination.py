from math import ceil
from typing import Callable, ClassVar, Type, TypeVar, Generic
from pydantic import BaseModel
# from pydantic.generics import GenericModel

DataT = TypeVar('DataT')

class PaginationMeta(BaseModel):
    page: int
    page_size: int
    total: int
    total_pages: int

class Pagination(BaseModel, Generic[DataT]):
    data: list[DataT]
    pagination: PaginationMeta

    total_pages: ClassVar[Callable[[int, int], int]] = ceil

    @classmethod
    def create(cls: Type['Pagination[DataT]'], data: list[DataT], page: int, page_size: int, total: int) -> 'Pagination[DataT]':
        pagination = PaginationMeta(page=page, page_size=page_size, total=total, total_pages=cls.total_pages(total, page_size))
        return cls(data=data, pagination=pagination)