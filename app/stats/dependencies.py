from typing import Annotated

from fast_depends import Depends

from app.stats.service import StatsService

StatsServiceDep = Annotated[StatsService, Depends(StatsService)]
