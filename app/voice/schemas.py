from enum import auto, StrEnum

from pydantic import ConfigDict

from app.base.schemas import BaseModel


class VoiceCommand(StrEnum):
    create_task = auto()
    show_tasks = auto()
    unknown = auto()


class VoiceResponse(BaseModel):
    speech_text: str
    cmd: VoiceCommand

    model_config = ConfigDict(extra="allow")
