from typing import Annotated

from aiogram import types
from fast_depends import Depends

from app.users.schemas import UserRead
from app.users.service import UserService

UserServiceDep = Annotated[UserService, Depends(UserService)]


async def get_current_user(event_from_user: types.User, service: UserServiceDep) -> UserRead:
    return await service.get_by_telegram_id(event_from_user.id)


MeDep = Annotated[UserRead, Depends(get_current_user)]
