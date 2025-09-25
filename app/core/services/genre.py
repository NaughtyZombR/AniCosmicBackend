from api.exceptions.genre import GenreNotFoundException
from core.models import Genre
from core.schemas.genre import GenreCreate, GenreUpdate
from core.services.base import ModelService
from core.services.repositories.genre import GenreRepository


class GenreService(ModelService[Genre, GenreCreate, GenreUpdate]):
    @property
    def model_repository(self) -> type[GenreRepository]:
        return GenreRepository

    @property
    def not_found_error(self) -> type[GenreNotFoundException]:
        return GenreNotFoundException

    def __init__(self, session):
        super().__init__(session)

    async def get_by_title(self, title: str) -> Genre | None:
        return await self._repository.get_by_title(title)
