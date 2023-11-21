from sqlalchemy.ext.asyncio import AsyncSession

from .repo import Repository
from ..models import Comment


class CommentRepo(Repository[Comment]):
    def __init__(self, session: AsyncSession):
        super().__init__(type_model=Comment, session=session)

    def new(
            self,
            text: str
    ) -> Comment:
        obj = Comment(
            text=text
        )
        self.session.add(obj)
        return obj
