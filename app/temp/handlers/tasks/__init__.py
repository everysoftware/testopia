from aiogram import Router

from .add import router as add_router
from .comment import router as comment_router
from .edit import router as edit_router
from .report import router as report_router
from .show import router as show_router
from .show_one import router as show_one_router
from ...middlewares import DatabaseMd

routers = (
    add_router,
    show_router,
    edit_router,
    comment_router,
    report_router,
    show_one_router,
)

router = Router(name="tasks")
router.include_routers(*routers)

router.message.middleware(DatabaseMd())
router.callback_query.middleware(DatabaseMd())
