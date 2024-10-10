from fast_depends import inject

from app.config import settings
from app.users.dependencies import UserServiceDep


@inject
async def register_admin(users: UserServiceDep) -> None:
    # Register admin
    if not settings.auth.admin_telegram_id:
        return
    user = await users.get_by_telegram_id(settings.auth.admin_telegram_id)
    if not user:
        await users.register(
            first_name="Admin",
            telegram_id=settings.auth.admin_telegram_id,
            is_superuser=True,
        )
