from pydantic import SecretStr
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    bot_token: SecretStr
    mode: str = "polling"  # "polling" or "webhook"
    drop_updates_on_restart: bool = False
    webhook_addr: str | None = None
    webhook_path: str = "/"
    webhook_secret: SecretStr = "aaaaa"


def get_config() -> Config:
    return Config()
