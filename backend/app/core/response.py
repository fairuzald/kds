from typing import Any, Dict, Generic, List, Optional, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class StandardResponse(BaseModel, Generic[T]):
    success: bool
    message: str
    data: Optional[T] = None
    error: Optional[Dict[str, Any]] = None
    model_config = {"from_attributes": True}


def success_response(
    data: Any = None,
    message: str = "Operation successful",
) -> StandardResponse:
    return StandardResponse(success=True, message=message, data=data)


def error_response(
    message: str = "An error occurred",
    error_detail: Optional[Any] = None,
) -> StandardResponse:
    error_content = {"detail": error_detail} if error_detail else None
    return StandardResponse(success=False, message=message, error=error_content)


class PaginationMeta(BaseModel):
    current_page: int
    page_size: int
    total_items: int
    total_pages: int
    has_previous: bool
    has_next: bool


class PaginatedResponseStructure(StandardResponse[List[T]], Generic[T]):
    meta: Optional[PaginationMeta] = None


def paginated_response(
    data: List[Any],
    total_items: int,
    page: int,
    page_size: int,
    message: str = "Data retrieved successfully",
) -> PaginatedResponseStructure:
    total_pages = (total_items + page_size - 1) // page_size if page_size > 0 else 0

    pagination_meta = PaginationMeta(
        current_page=page,
        page_size=page_size,
        total_items=total_items,
        total_pages=total_pages,
        has_previous=page > 1,
        has_next=page < total_pages,
    )

    return PaginatedResponseStructure(
        success=True,
        message=message,
        data=data,
        meta=pagination_meta,
    )
