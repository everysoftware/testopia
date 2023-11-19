from sqlalchemy.ext.asyncio import AsyncSession

from .repo import Repository
from ..models import Task


class TaskRepo(Repository[Task]):
    def __init__(self, session: AsyncSession):
        super().__init__(type_model=Task, session=session)

    def new(
            self,
            user_id: int,
            checklist_id: int,
            name: str,
    ) -> Task:
        obj = Task(
            user_id=user_id,
            checklist_id=checklist_id,
            name=name,
        )
        self.session.add(obj)
        return obj
