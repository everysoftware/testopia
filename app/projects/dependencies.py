from typing import Annotated

from fast_depends import Depends

from app.projects.service import ProjectUseCases

ProjectServiceDep = Annotated[ProjectUseCases, Depends(ProjectUseCases)]
