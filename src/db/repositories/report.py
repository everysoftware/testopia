from sqlalchemy.ext.asyncio import AsyncSession

from .repo import Repository
from ..models import Report


class ReportRepo(Repository[Report]):
    def __init__(self, session: AsyncSession):
        super().__init__(type_model=Report, session=session)

    def new(
            self,
            task_id: int,
            url: str
    ) -> Report:
        obj = Report(
            task_id=task_id,
            url=url
        )
        self.session.add(obj)
        return obj
