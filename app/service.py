from abc import ABC

from app.ai.dependencies import AIDep
from app.db.dependencies import UOWDep


class Service(ABC):
    def __init__(self, uow: UOWDep, ai: AIDep) -> None:
        self.uow = uow
        self.ai = ai
