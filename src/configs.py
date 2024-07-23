import logging
from functools import cached_property
from pydantic_settings import BaseSettings, SettingsConfigDict


class GigachatConfig(BaseSettings):
    gigachat_client_secret: str
    gigachat_client_id: str
    gigachat_auth_data: str

    model_config = SettingsConfigDict(env_file="./.env")


class AppConfig(BaseSettings):
    host: str = "0.0.0.0"
    port: int = 8000
    reload: bool = False
    logging_level: int = logging.DEBUG
    proxy_headers: bool = True

    @cached_property
    def get_uvicorn_attr(self) -> dict[str, str | bool | None]:
        return {
            "host": self.host,
            "port": self.port,
            "reload": self.reload,
            "log_level": self.logging_level,
            "proxy_headers": self.proxy_headers
        }


GIGACHAT_CONFIG = GigachatConfig()
APP_CONFIG = AppConfig()
