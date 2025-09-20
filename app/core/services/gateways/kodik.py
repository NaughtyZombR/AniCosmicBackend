import logging
from httpx import AsyncClient, HTTPStatusError

from api.exceptions.llm import (
    LLMBadResponseException,
    LLMModelNotFoundException,
)
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
        """
        Поиск аниме по названию с жёстким соответствием и своей озвучкой.
        """
        async with self._client as client:
            response = await client.get(
                "/search",
                params={
                    "type": 5,
                    "title": title,
                    "strict": "true",
                    "translation_id": 2700,
                    "token": self._token,
                },
            )

        try:
            response.raise_for_status()
        except HTTPStatusError as e:
            status_class = response.status_code // 100
            if status_class == 4:
                raise LLMModelNotFoundException() from e
            else:
                raise LLMBadResponseException() from e

        return response.json()

    async def list_content(self) -> dict:
        """
        Получение списка по озвучке.
        https://kodikapi.com/list
        """
        async with self._client as client:
            response = await client.get(
                "/list",
                params={
                    "type": 5,
                    "translation_id": 2700,
                    "token": self._token,
                },
            )

        try:
            response.raise_for_status()
        except HTTPStatusError as e:
            status_class = response.status_code // 100
            if status_class == 4:
                raise LLMModelNotFoundException() from e
            else:
                raise LLMBadResponseException() from e

        return response.json()
