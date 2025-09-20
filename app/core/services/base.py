from abc import abstractmethod

from api.exceptions.base import NotFoundException
from core.models.base import BaseModel
from core.schemas.base import BaseSchema
from core.services.repositories.SQLAlchemy import SQLAlchemyRepository
from sqlalchemy.ext.asyncio import AsyncSession


class ModelService[
    TModel: BaseModel,
    TCreateSchema: BaseSchema,
    TUpdateSchema: BaseSchema,
]:
    @property
    @abstractmethod
    def model_repository(self) -> type[SQLAlchemyRepository]: ...

    @property
    @abstractmethod
    def not_found_error(self) -> type[NotFoundException]: ...

    @property
    def model(self) -> type[TModel]:
        return self._repository.model

    def __init__(self, session: AsyncSession):
        self._repository = self.model_repository(session)

    async def create(self, schema: TCreateSchema) -> TModel:
        created = await self._repository.create(schema)
        return created

    async def get_by_id(
        self,
        model_id,
    ) -> TModel:
        existing = await self._repository.get_by_pk(model_id)
        if not existing:
            raise self.not_found_error
        return existing

    async def is_exist_with_id(self, model_id) -> bool:
        existing = await self.get_by_id(model_id)
        return existing is not None

    async def update_by_id(self, model_id, schema: TUpdateSchema) -> TModel:
        updated = await self._repository.update_by_pk(model_id, schema)
        if not updated:
            raise self.not_found_error
        return updated

    async def delete_by_id(self, model_id) -> TModel:
        deleted = await self._repository.delete_by_pk(model_id)
        if not deleted:
            raise self.not_found_error
        return deleted

    async def save_changes(self) -> None:
        await self._repository.commit()
