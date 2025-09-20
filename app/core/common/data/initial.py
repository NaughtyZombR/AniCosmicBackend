from database import async_session_maker


async def load_initial_data() -> None:
    async with async_session_maker():
        # здесь создаются сервисы и загружаются необходимые данные
        pass
