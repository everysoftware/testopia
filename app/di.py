from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware, Dispatcher
from aiogram.dispatcher.event.handler import HandlerObject
from aiogram.types import TelegramObject
from fast_depends import inject as fast_inject


def inject[T, **P](
    func: Callable[P, Awaitable[T]], **kwargs: Any
) -> Callable[P, Awaitable[T]]:
    async def wrapper(*args: P.args, **real_kwargs: P.kwargs) -> T:
        injected = fast_inject(func)
        real_kwargs |= kwargs  # type: ignore[assignment]
        return await injected(
            *args,
            **real_kwargs,
        )

    return wrapper


class DIMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        real_handler: HandlerObject = data["handler"]
        real_handler.callback = inject(real_handler.callback, **data)
        data["handler"] = real_handler
        return await handler(event, data)


def setup_di(dp: Dispatcher) -> None:
    dp.message.middleware(DIMiddleware())
    dp.callback_query.middleware(DIMiddleware())
