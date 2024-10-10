from app.db.types import ID
from app.service import Service
from app.users.schemas import (
    UserRead,
)


class UserService(Service):
    async def get_by_telegram_id(self, telegram_id: int) -> UserRead | None:
        return await self.uow.users.get_by_telegram_id(telegram_id)

    async def get_one_by_telegram_id(self, telegram_id: int) -> UserRead:
        user = await self.get_by_telegram_id(telegram_id)
        if not user:
            raise ValueError()
        return user

    async def register(
        self,
        *,
        telegram_id: int,
        first_name: str,
        last_name: str | None = None,
        is_superuser: bool = False,
    ) -> UserRead:
        if telegram_id and (await self.get_by_telegram_id(telegram_id)):
            raise ValueError()
        user = await self.uow.users.create(
            is_superuser=is_superuser,
            first_name=first_name,
            last_name=last_name,
            telegram_id=telegram_id,
        )
        return user

    async def get(self, user_id: ID) -> UserRead | None:
        return await self.uow.users.get(user_id)

    async def get_one(self, user_id: ID) -> UserRead:
        user = await self.get(user_id)
        if not user:
            raise ValueError()
        return user
