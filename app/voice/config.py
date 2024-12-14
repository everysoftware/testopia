from app.base.schemas import BaseSettings


class VoiceSettings(BaseSettings):
    recognition_model: str = "./models/vosk-rus"


voice_settings = VoiceSettings()
