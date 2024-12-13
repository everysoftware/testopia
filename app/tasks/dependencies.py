from typing import Annotated

from fast_depends import Depends

from app.tasks.service import TaskUseCases

TaskServiceDep = Annotated[TaskUseCases, Depends(TaskUseCases)]
