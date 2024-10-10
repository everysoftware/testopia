from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.dispatcher.event.handler import HandlerObject
from aiogram.types import TelegramObject
from fast_depends import inject as fast_inject


def inject[T, ** P](func: Callable[P, T], **kwargs: Any) -> Callable[P, T]:
    async def wrapper(*args: Any, **_kwargs: Any):
        injected = fast_inject(func)
        _kwargs |= kwargs
        return await injected(
            *args,
            **_kwargs,
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
