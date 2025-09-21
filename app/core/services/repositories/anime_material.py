from collections.abc import Sequence
from typing import override
from uuid import UUID

from core.models import AnimeMaterial
from core.schemas.anime_material import AnimeMaterialUpdate
from core.services.repositories.SQLAlchemy import SQLAlchemyRepository
from sqlalchemy import ColumnElement


class AnimeMaterialRepository(
    SQLAlchemyRepository[AnimeMaterial, None, AnimeMaterialUpdate]
):
    @property
    def model_pk(self) -> UUID:
        return AnimeMaterial.id

    @override
    @property
    def model(self) -> type[AnimeMaterial]:
        return AnimeMaterial

    @staticmethod
    def default_order_by() -> Sequence[ColumnElement]:
        return [AnimeMaterial.created_at.desc()]
