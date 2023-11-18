from aiogram import Router

from .show import router as show_pie_router
from ...middlewares import DatabaseMd

routers = (
    show_pie_router,
)

router = Router(name='stats')
router.include_routers(*routers)

router.message.middleware(DatabaseMd())
router.callback_query.middleware(DatabaseMd())
