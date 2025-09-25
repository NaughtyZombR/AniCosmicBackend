from abc import abstractmethod
from collections.abc import Sequence

from core.models.base import BaseModel
from core.schemas.base import BaseSchema, DictStrAny
from sqlalchemy import ColumnElement, delete, func, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.base import ExecutableOption


class SQLAlchemyRepository[
    TModel: BaseModel,
    TCreateSchema: BaseSchema,
    TUpdateSchema: BaseSchema,
]:
    @property
    @abstractmethod
    def model(self) -> type[TModel]: ...

    @property
    @abstractmethod
    def model_pk(self): ...

    def __init__(self, session: AsyncSession):
        self._session = session

    async def create(self, schema: TCreateSchema | DictStrAny) -> TModel:
        schema = self.__schema_to_dict(schema)
        obj = self.model(**schema)
        self._session.add(obj)
        await self._session.flush()
        return obj

    async def create_many(
        self, schemas: Sequence[TCreateSchema | DictStrAny]
    ) -> list[TModel]:
        schemas = [self.__schema_to_dict(schema) for schema in schemas]
        objs = [self.model(**schema) for schema in schemas]
        self._session.add_all(objs)
        await self._session.flush()
        return objs

    async def create_from_orm(self, obj: TModel) -> TModel:
        self._session.add(obj)
        await self._session.flush()
        return obj

    # async def create_if_not_exists(
    #     self,
    #     schema: _CreateSchema | DictStrAny,
    #     criteria: Sequence[ColumnElement[bool]] = (),
    # ) -> _Model:
    #     schema = self.__schema_to_dict(schema)
    #     if await self.get_one_where(where=criteria):
    #         return await self.get_one_where(criteria)
    #     return await self.create(schema)

    async def get_all(
        self,
        where: Sequence[ColumnElement[bool]] = (),
        order_by: Sequence[ColumnElement] = (),
        options: Sequence[ExecutableOption] = (),
        offset: int = 0,
        limit: int = 100,
    ) -> Sequence[TModel]:
        stmt = (
            select(self.model)
            .where(*where)
            .order_by(*order_by)
            .options(*options)
            .offset(offset)
            .limit(limit)
        )
        result = await self._session.execute(stmt)
        lazy_entities = result.scalars().unique()
        return lazy_entities.all()

    async def count(
        self,
        where: Sequence[ColumnElement[bool]] = (),
        options: Sequence[ExecutableOption] = (),
    ) -> int:
        stmt = (
            select(func.count())
            .select_from(self.model)
            .where(*where)
            .options(*options)
        )
        result = await self._session.execute(stmt)
        count = result.scalar()
        return count

    async def get_one_where(
        self,
        where: Sequence[ColumnElement[bool]],
        options: Sequence[ExecutableOption] = (),
    ) -> TModel | None:
        result = await self.get_all(
            where=where,
            options=options,
            limit=1,
        )
        return result[0] if result else None

    async def get_by_pk(
        self,
        pk,
    ) -> TModel | None:
        result = await self._session.get(self.model, pk)
        return result

    async def update_all_where(
        self,
        schema: TUpdateSchema | DictStrAny,
        where: Sequence[ColumnElement[bool]] = (),
    ) -> Sequence[TModel]:
        schema = self.__schema_to_dict(schema)
        stmt = (
            update(self.model)
            .where(*where)
            .values(**schema)
            .returning(self.model)
        )
        result = await self._session.execute(stmt)
        await self._session.flush()
        return result.scalars().all()

    async def update_by_pk(
        self,
        pk,
        schema: TUpdateSchema | DictStrAny,
    ) -> TModel | None:
        result = await self.update_all_where(
            schema,
            where=[self.model_pk == pk],  # noqa
        )
        return result[0] if result else None

    async def update_from_orm(
        self,
        obj: TModel | Sequence[TModel],
    ) -> None:
        obj = obj if isinstance(obj, Sequence) else [obj]
        await self._session.flush(obj)

    async def delete_all_where(
        self,
        where: Sequence[ColumnElement[bool]] = (),
    ) -> Sequence[TModel]:
        stmt = delete(self.model).where(*where).returning(self.model)
        result = await self._session.execute(stmt)
        await self._session.flush()
        return result.scalars().all()

    async def delete_one_where(
        self,
        where: Sequence[ColumnElement[bool]],
    ) -> TModel | None:
        result = await self.delete_all_where(
            where=where,
        )
        return result[0] if result else None

    async def delete_by_pk(
        self,
        pk,
    ) -> TModel | None:
        result = await self.delete_all_where(
            where=[self.model_pk == pk],  # noqa
        )
        return result[0] if result else None

    async def delete_from_orm(
        self,
        obj: TModel,
    ) -> None:
        await self._session.delete(obj)
        await self._session.flush()

    async def delete_many_from_orm(
        self,
        objs: Sequence[TModel],
    ) -> None:
        for obj in objs:
            await self._session.delete(obj)
        await self._session.flush()

    async def refresh(self, obj: TModel) -> None:
        await self._session.refresh(obj)

    async def rollback(self) -> None:
        await self._session.rollback()

    async def commit(self) -> None:
        await self._session.commit()

    @staticmethod
    def __schema_to_dict(
        schema: TUpdateSchema | DictStrAny,
    ) -> DictStrAny:
        if isinstance(schema, BaseSchema):
            return schema.model_dump()
        return schema
