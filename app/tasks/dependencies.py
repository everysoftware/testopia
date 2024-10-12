from typing import Annotated

from fast_depends import Depends

from app.tasks.service import TaskService

TaskServiceDep = Annotated[TaskService, Depends(TaskService)]
