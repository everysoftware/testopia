from sqlalchemy.ext.asyncio import AsyncSession

from .repo import Repository
from ..models.product import Product


class ProductRepo(Repository[Product]):
    def __init__(self, session: AsyncSession):
        super().__init__(type_model=Product, session=session)

    def new(self, owner_id: int, name: str) -> Product:
        obj = Product(owner_id=owner_id, name=name)
        self.session.add(obj)
        return obj
