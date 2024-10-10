from typing import Annotated

from fast_depends import Depends

from app.devices.service import DeviceService
from app.tasks.service import TaskService

TaskServiceDep = Annotated[TaskService, Depends(TaskService)]
