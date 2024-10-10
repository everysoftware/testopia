from typing import Annotated

from fast_depends import Depends

from app.checklists.service import ChecklistService

ChecklistServiceDep = Annotated[ChecklistService, Depends(ChecklistService)]
