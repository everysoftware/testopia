from .checklists import router as checklists_router
from .devices import router as devices_router
from .main import router as main_router
from .products import router as products_router
from .stats import router as stats_router
from .tasks import router as tasks_router

routers = (
    main_router,
    products_router,
    devices_router,
    checklists_router,
    tasks_router,
    stats_router,
)

__all__ = ("routers",)
