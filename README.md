# AniCosmicBackend

## Запуск

1. Создайте файл ```.env``` в корне проекта на основе ```example.env```
2. Запустите команду ```docker compose up --build -d```

## Разработка

1. Создать окружение poetry ```poetry env activate```
2. Установить зависимости ```poetry install --with=dev```
3. Установить pre-commit хуки ```pre-commit install```
4. Создайте файл ```.env``` в корне проекта на основе ```example.env```
5. Запустить контейнер с БД ```docker-compose up db -d```
6. Для локального запуска приложения перейти в директорию ```app``` и
   запустить скрипт launch.py ```python launch.py```. Для запуска приложения
   в контейнере ```docker-compose up api -d```

- Запуск линтера ```ruff check```
- Запуск форматтера ```ruff format```
- Запуск тестов ```pytest```
