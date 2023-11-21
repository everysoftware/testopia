# Testopia

Сделайте тестирование Вашего проекта лучше с системой тестирования Testopia!  
[![Lint](https://github.com/everysoftware/testopia/actions/workflows/ci.yml/badge.svg)](https://github.com/everysoftware/testopia/actions/workflows/ci.yml)

<img src="https://github.com/everysoftware/testopia/assets/22497421/88a12221-714e-460c-bf6f-55c66869143e" width="250" />  
<img src="https://github.com/everysoftware/testopia/assets/22497421/3daca09d-3510-424d-98e9-7651044218d7" width="250" />  
<img src="https://github.com/everysoftware/testopia/assets/22497421/382e5b1e-2da7-43e8-afe5-12180835a3c4" width="250" />  

## Начало работы
1. Запустите бота
2. Добавяйте свои устройства и программные продукты для тестирования
3. Создавайте и управляете задачами тестирования проекта
4. Отслеживайте статистику прохождения тестов
5. Готово!

## Стек технологий

Python3 • Aiogram3 • PostgreSQL • SQLAlchemy 2 • Alembic • Redis • arq • Aiottp • Docker • Ruff • Pandas • Matplotlib  
[Макеты Figma](https://www.figma.com/file/iJ7SMg6DCuCaDhNlieh3kd/Untitled?type=design&node-id=0-1&mode=design)

## Сборка

1. Создайте файл окружения ```.env```.
```
BOT_MODE="docker"


BOT_DEBUG=0
BOT_LOGGING_LEVEL="INFO"

BOT_TELEGRAM_TOKEN="YOUR_BOT_TELEGRAM_TOKEN"

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

WEBHOOK_ON=0
WEBHOOK_HOST="localhost"
WEBHOOK_PORT=8080
WEBHOOK_URL="YOUR_WEBHOOK_URL"
   ```
3. Соберите и запустите контейнеры Docker: ```docker-compose up -d --build```
4. Готово!

**Иконка приложения создана искусственным интеллектом.**  
**Разработано специально для хакатона в рамках всероссийского конкурса "Студент года IT".** 

**Made with ❤️ by @ivanstasevich**
