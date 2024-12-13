from typing import Annotated

from fast_depends import Depends

from app.workspaces.service import WorkspaceUseCases

WorkspaceServiceDep = Annotated[WorkspaceUseCases, Depends(WorkspaceUseCases)]
