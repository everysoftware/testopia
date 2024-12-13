from typing import Annotated

from fast_depends import Depends

from app.voice.service import VoiceUseCases

VoiceServiceDep = Annotated[VoiceUseCases, Depends(VoiceUseCases)]
