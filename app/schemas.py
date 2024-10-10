from pydantic import BaseModel, ConfigDict
from pydantic_settings import BaseSettings as PydanticBaseSettings, SettingsConfigDict


class BackendBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class BaseSettings(PydanticBaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="allow")
