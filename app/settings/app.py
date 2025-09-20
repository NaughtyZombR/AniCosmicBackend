from settings.base import CommonBaseSettings


class ApplicationSettings(CommonBaseSettings):
    allowed_origins: list[str] = [
        "http://127.0.0.1",
        "http://127.0.0.1:80",
        "http://localhost:3000",
        "http://localhost:5173",
    ]
    host: str = "0.0.0.0"
    port: int = 8000


app_settings = ApplicationSettings()
