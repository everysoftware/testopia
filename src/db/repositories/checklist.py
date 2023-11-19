from sqlalchemy.ext.asyncio import AsyncSession

from .repo import Repository
from ..models.checklist import Checklist


class ChecklistRepo(Repository[Checklist]):
    def __init__(self, session: AsyncSession):
        super().__init__(type_model=Checklist, session=session)

    def new(
            self,
            name: str,
            product_id: int
    ) -> Checklist:
        obj = Checklist(
            product_id=product_id,
            name=name
        )
        self.session.add(obj)
        return obj
