from core.schemas.anime_material import AnimeMaterialCreate
from core.services.gateways.kodik import KodikGateway
from settings.kodik import KodikAPISettings


class KodikService:
    def __init__(self, settings: KodikAPISettings) -> None:
        self._kodik_gateway = KodikGateway(settings)

    async def get_anime_material_schema(
        self, title: str
    ) -> AnimeMaterialCreate | None:
        """
        Получение материала по названию через Kodik API.
        Возвращает Pydantic-схему AnimeMaterialCreate или None.
        """
        data = await self._kodik_gateway.search_by_title(title)
        results = data.get("results", [])
        if not results:
            return None

        if results and isinstance(results[0], dict):
            material_json = results[0].get("material_data", {})
        else:
            material_json = {}

        # Добавляем данные о выпущенных сериях, если есть
        if "last_episode" in results[0]:
            material_json["released_episodes_count"] = results[0][
                "last_episode"
            ]

        # Pydantic сам забирает только нужные поля
        material_schema = AnimeMaterialCreate.model_validate(material_json)
        return material_schema
