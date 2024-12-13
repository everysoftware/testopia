from app.base.use_case import UseCase
from app.db.dependencies import UOWDep
from app.projects.models import Project
from app.users.config import auth_settings
from app.users.models import User
from app.users.repositories import TelegramUserSpecification
from app.users.schemas import (
    UserCreate,
)
from app.workspaces.models import Workspace


class AuthUseCases(UseCase):
    def __init__(self, uow: UOWDep) -> None:
        self.uow = uow

    async def get_by_telegram_id(self, telegram_id: int) -> User | None:
        return await self.uow.users.find(
            TelegramUserSpecification(telegram_id)
        )

    async def get_one_by_telegram_id(self, telegram_id: int) -> User:
        return await self.uow.users.find_one(
            TelegramUserSpecification(telegram_id)
        )

    async def register(self, data: UserCreate) -> User:
        if await self.get_by_telegram_id(data.telegram_id):
            raise ValueError()
        user = User.from_dto(data)
        if user.telegram_id == auth_settings.admin_telegram_id:
            user.grant_superuser()
        workspace = Workspace(
            name="Личное пространство",
            description="Личное пространство, которое создалось при регистрации в Testopia",
            user=user,
        )
        project = Project(
            name="Стандартный",
            description="Стандартный проект, который создался при регистрации в Testopia",
            workspace=workspace,
            user=user,
        )
        await self.uow.users.add(user)
        await self.uow.workspaces.add(workspace)
        await self.uow.projects.add(project)
        await self.uow.commit()
        return user
