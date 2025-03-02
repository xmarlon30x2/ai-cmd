from os import getenv
from typing import Any, Optional

from dotenv import load_dotenv
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings

from .const import ENV_FILE
from .exceptions import ConfigError


class SingeltonSettings:
    instance: "Settings | None" = None


class Settings(BaseSettings):
    api_key: str
    api_key_reasoner: str
    model: str = "deepseek"
    base_url: str = "https://deepseek.com/"
    model_reasoner: str = "deepseek-reasoner"
    base_url_reasoner: str = "https://deepseek.com/"
    temperature: float = Field(0.6, ge=0, le=1)
    temperature_reasoner: float = Field(0.6, ge=0, le=1)
    instance: Optional["Settings"] = None

    @staticmethod
    def temperature_must_be_valid(value: Any) -> int | float:
        if not isinstance(value, (int, float)):
            raise ValueError("Temperature must be a number")
        if not 0 <= value <= 1:
            raise ValueError("Temperature must be between 0 and 1")
        return value

    field_validator("temperature")(temperature_must_be_valid)
    field_validator("temperature_reasoner")(temperature_must_be_valid)

    @classmethod
    def load_env(cls) -> dict[str, Any]:
        try:
            load_dotenv(ENV_FILE)
            api_key = getenv("api_key")
            api_key_reasoner = getenv("api_key_reasoner")
            model = getenv("model")
            base_url = getenv("base_url")
            temperature = getenv("temperature")
            model_reasoner = getenv("model_reasoner")
            base_url_reasoner = getenv("base_url_reasoner")
            temperature_reasoner = getenv("temperature_reasoner")
            return {
                "model": model,
                "api_key": api_key,
                "base_url": base_url,
                "temperature": temperature,
                "model_reasoner": model_reasoner,
                "api_key_reasoner": api_key_reasoner,
                "base_url_reasoner": base_url_reasoner,
                "temperature_reasoner": temperature_reasoner,
            }
        except Exception as e:
            raise ConfigError(
                f"Error loading environment variables from {ENV_FILE}: {e}"
            )

    @classmethod
    def get_instance(cls) -> "Settings":
        if not SingeltonSettings.instance:
            kwargs = cls.load_env()
            try:
                SingeltonSettings.instance = Settings(**kwargs)
            except ValueError as e:
                raise ConfigError(f"Error validating environment variables: {e}")
        return SingeltonSettings.instance

    def save(self):
        data = self.model_dump()
        data.pop("instance", None)
        content = "\n".join([f"{key} = {value}" for (key, value) in data.items()])
        with open(ENV_FILE, "w", encoding="utf-8") as file:
            file.write(content)
