import logging

from api.exceptions.external_api import KodikBadResponseException
from httpx import AsyncClient, HTTPStatusError
from settings.kodik import KodikAPISettings

logger = logging.getLogger(__name__)


class KodikGateway:
    def __init__(self, settings: KodikAPISettings) -> None:
        self._base_url = settings.host.unicode_string()
        self._token = settings.token
        self._translation_id = settings.translation_id
        self._client_instance: AsyncClient | None = None

    @property
    def _client(self) -> AsyncClient:
        """
        Создаёт и возвращает новый клиент или возвращает существующий,
        если он не закрыт
        """
        if self._client_instance is None or self._client_instance.is_closed:
            self._client_instance = AsyncClient(base_url=self._base_url)
        return self._client_instance

    async def search_by_title(self, title: str) -> dict:
        """Поиск аниме по названию с материалом и эпизодами"""
        async with self._client as client:
            response = await client.get(
                "/search",
                params={
                    "type": 5,
                    "title": title,
                    "strict": "true",
                    "translation_id": self._translation_id,
                    "with_material_data": "true",
                    "with_episodes": "true",
                    "token": self._token,
                },
            )
        try:
            response.raise_for_status()
        except HTTPStatusError as e:
            raise KodikBadResponseException() from e
        return response.json()

    async def list_content(self, next_page: str | None = None) -> dict:
        """
        Получение списка по озвучке с поддержкой пагинации.
        Если передан next_page, делаем запрос именно к этой странице.
        """
        url = "/list" if not next_page else next_page

        async with self._client as client:
            response = await client.get(
                url,
                params={
                    "type": 5,
                    "translation_id": self._translation_id,
                    "with_material_data": "true",
                    "with_episodes": "true",
                    "token": self._token,
                },
            )

        try:
            response.raise_for_status()
        except HTTPStatusError as e:
            raise KodikBadResponseException() from e

        return response.json()
