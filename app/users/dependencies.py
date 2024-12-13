from typing import Annotated

from aiogram import types
from fast_depends import Depends

from app.users.models import User
from app.users.service import AuthUseCases

UserServiceDep = Annotated[AuthUseCases, Depends(AuthUseCases)]


async def get_current_user(
    event_from_user: types.User, users: UserServiceDep
) -> User:
    return await users.get_one_by_telegram_id(event_from_user.id)


UserDep = Annotated[User, Depends(get_current_user)]
