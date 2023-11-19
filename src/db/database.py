from sqlalchemy.ext.asyncio import AsyncSession

from src.db.repositories import (
    CommentRepo,
    TaskRepo,
    UserRepo,
    ReportRepo,
    DeviceRepo,
    ProductRepo,
    ChecklistRepo
)


class Database:
    session: AsyncSession
    comment: CommentRepo
    task: TaskRepo
    report: ReportRepo
    device: DeviceRepo
    product: ProductRepo
    checklist: ChecklistRepo

    def __init__(self, session: AsyncSession):
        self.session = session

        self.comment = CommentRepo(session=session)
        self.user = UserRepo(session=session)
        self.checklist = ChecklistRepo(session=session)
        self.task = TaskRepo(session=session)
        self.report = ReportRepo(session=session)
        self.device = DeviceRepo(session=session)
        self.product = ProductRepo(session=session)
