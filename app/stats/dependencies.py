from typing import Annotated

from fast_depends import Depends

from app.stats.service import StatsUseCases

StatsServiceDep = Annotated[StatsUseCases, Depends(StatsUseCases)]
