from pydantic_settings import BaseSettings, SettingsConfigDict


class GigachatConfig(BaseSettings):
    gigachat_client_secret: str
    gigachat_auth_data: str

    model_config = SettingsConfigDict(env_file="./.env")


GIGACHAT_CONFIG = GigachatConfig()
