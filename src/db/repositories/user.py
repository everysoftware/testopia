from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from .repo import Repository
from ..models import User


class UserRepo(Repository[User]):
    def __init__(self, session: AsyncSession):
        super().__init__(type_model=User, session=session)

    def new(
        self,
        user_id: int,
        first_name: str,
        language_code: Optional[str] = None,
        last_name: Optional[str] = None,
        username: Optional[str] = None,
    ) -> User:
        obj = User(
            user_id=user_id,
            first_name=first_name,
            last_name=last_name,
            language_code=language_code,
            username=username,
        )
        self.session.add(obj)
        return obj
