import asyncio
import logging

from aiogram import Bot, Dispatcher, Router
from aiogram.fsm.storage.redis import RedisStorage

from app.cache.connection import redis_client
from app.cache.lifespan import ping_redis
from app.commands import BOT_COMMANDS
from app.config import settings
from app.middlewares import DIMiddleware
from app.users.lifespan import register_admin
from app.users.handlers import router as start_router
from app.checklists.handlers import router as checklists_router
from app.tasks.handlers import router as tasks_router
from app.devices.handlers import router as devices_router
from .bot import bot as tg_bot

routers = [start_router, checklists_router, tasks_router, devices_router]

main_router = Router()
main_router.message.middleware(DIMiddleware())
main_router.callback_query.middleware(DIMiddleware())
main_router.include_routers(*routers)


async def on_startup(bot: Bot, dispatcher: Dispatcher) -> None:
    await ping_redis()
    await register_admin()  # type: ignore[call-arg]
    await bot.set_my_commands(BOT_COMMANDS)


async def on_shutdown(bot: Bot, dispatcher: Dispatcher) -> None:
    pass


storage = RedisStorage(redis=redis_client, state_ttl=settings.cache.state_ttl, data_ttl=settings.cache.data_ttl)
dp = Dispatcher(storage=storage)
dp.include_router(main_router)
dp.startup.register(on_startup)
dp.shutdown.register(on_shutdown)


def main() -> None:
    logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)
    logging.basicConfig(level=logging.INFO)
    asyncio.run(dp.start_polling(tg_bot))


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, SystemExit):
        logging.info("Bot stopped")
