import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage

from app.cache.connection import redis_client
from app.cache.lifespan import ping_redis
from app.commands import BOT_COMMANDS
from app.config import settings
from app.di import setup_di
from app.routing import main_router
from app.users.lifespan import register_admin

from .bot import bot as tg_bot


async def on_startup(bot: Bot, dispatcher: Dispatcher) -> None:
    await ping_redis()
    await register_admin()  # type: ignore[call-arg]
    await bot.set_my_commands(BOT_COMMANDS)
    os.makedirs(settings.stats.stats_dir, exist_ok=True)


async def on_shutdown(bot: Bot, dispatcher: Dispatcher) -> None:
    pass


storage = RedisStorage(redis=redis_client, state_ttl=settings.cache.state_ttl, data_ttl=settings.cache.data_ttl)
dp = Dispatcher(storage=storage)
setup_di(dp)
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
