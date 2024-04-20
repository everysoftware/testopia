from sqlalchemy.ext.asyncio import AsyncSession

from .repo import Repository
from ..models import Report


class ReportRepo(Repository[Report]):
    def __init__(self, session: AsyncSession):
        super().__init__(type_model=Report, session=session)

    def new(self, url: str) -> Report:
        obj = Report(url=url)
        self.session.add(obj)
        return obj
