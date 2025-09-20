"""
Скрипт предназначен для локального запуска API
"""

import uvicorn
from main import app
from settings.app import app_settings


def main():
    config = uvicorn.Config(
        app=app, host=app_settings.host, port=app_settings.port
    )
    server = uvicorn.Server(config)
    server.run()


if __name__ == "__main__":
    main()
