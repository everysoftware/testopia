# Testopia

Сделайте тестирование Вашего проекта лучше с системой тестирования Testopia!  
[![Lint](https://github.com/everysoftware/testopia/actions/workflows/ci.yml/badge.svg)](https://github.com/everysoftware/testopia/actions/workflows/ci.yml)

## Начало работы
1. Запустите бота
2. Добавяйте свои устройства и программные продукты для тестирования
3. Создавайте и управляете задачами тестирования проекта
4. Готово!

## Стек технологий

Python3 • Aiogram3 • PostgreSQL • SQLAlchemy 2 • Alembic • Redis • arq • Aiottp • Docker • Ruff • Pandas • Matplotlib

## Сборка

1. Создайте файл окружения ```.env```.
```
BOT_MODE="docker"

BOT_DEBUG=0
BOT_LOGGING_LEVEL="INFO"

BOT_TELEGRAM_TOKEN="YOUR_BOT_TELEGRAM_TOKEN"

WEBHOOK_ON=0
WEBHOOK_HOST="localhost"
WEBHOOK_PORT=8080
WEBHOOK_URL="YOUR_WEBHOOK_URL"

POSTGRES_DB="postgres"
POSTGRES_HOST="db"
POSTGRES_PASSWORD="postgres"
POSTGRES_PORT=5432
POSTGRES_USER="postgres"

REDIS_DATABASE=1
REDIS_USERNAME="default"
REDIS_PASSWORD="redis"
REDIS_PORT=6379
REDIS_HOST="redis"
REDIS_TTL_STATE=43200
REDIS_TTL_DATA=43200

   ```
3. Соберите и запустите контейнеры Docker: ```docker-compose up -d --build```
4. Готово!


**Made with ❤️ by @ivanstasevich**
