from sqlalchemy.ext.asyncio import AsyncSession

from .repo import Repository
from ..models.task_list import TaskList


class TaskListRepo(Repository[TaskList]):
    def __init__(self, session: AsyncSession):
        super().__init__(type_model=TaskList, session=session)

    def new(
            self,
            name: str,
            product_id: int
    ) -> TaskList:
        obj = TaskList(
            product_id=product_id,
            name=name
        )
        self.session.add(obj)
        return obj
