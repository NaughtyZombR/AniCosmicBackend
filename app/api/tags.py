from enum import StrEnum


class APITags(StrEnum):
    Auth: str = "Аутентификация"
    Email: str = "Почта"
    Post: str = "Пост"
    Misc: str = "Прочее"
    User: str = "Пользователь"
