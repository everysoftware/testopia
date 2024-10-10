from typing import Annotated

from fast_depends import Depends

from app.devices.service import DeviceService

DeviceServiceDep = Annotated[DeviceService, Depends(DeviceService)]
