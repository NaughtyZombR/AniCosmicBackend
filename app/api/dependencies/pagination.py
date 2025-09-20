from typing import Annotated

from core.schemas.pagination import PaginationParams
from fastapi import Depends

PaginationQueryParams = Annotated[PaginationParams, Depends(PaginationParams)]
