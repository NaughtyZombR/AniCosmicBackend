from dataclasses import dataclass
from typing import Sequence

from core.models.base import BaseModel


@dataclass
class ItemsPage[Model: BaseModel]:
    items: Sequence[Model]

    page: int
    per_page: int
    total: int
