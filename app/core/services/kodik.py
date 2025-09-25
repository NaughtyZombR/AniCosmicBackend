from core.schemas.external.kodik import KodikMaterialData
from core.services.gateways.kodik import KodikGateway
from settings.kodik import KodikAPISettings


class KodikService:
    def __init__(self, settings: KodikAPISettings) -> None:
        self._kodik_gateway = KodikGateway(settings)

    async def get_anime_material_data(
        self, title: str
    ) -> KodikMaterialData | None:
        """
        Получение материала по названию через Kodik API.
        Возвращает Pydantic-схему KodikMaterialData или None.
        """
        data = await self._kodik_gateway.search_by_title(title)
        results = data.get("results", [])
        if not results:
            return None

        material_json = (
            results[0].get("material_data", {})
            if isinstance(results[0], dict)
            else {}
        )

        # Добавляем данные о выпущенных сериях, если есть
        if "last_episode" in results[0]:
            material_json["episodes_aired"] = results[0]["last_episode"]

        return KodikMaterialData.model_validate(material_json)
