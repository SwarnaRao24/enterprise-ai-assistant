from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    openai_api_key: str = Field(validation_alias="OPENAI_API_KEY")
    openai_model: str = Field(default="gpt-5", validation_alias="OPENAI_MODEL")
    app_env: str = Field(default="dev", validation_alias="APP_ENV")
    log_path: str = Field(default="logs/interactions.jsonl", validation_alias="LOG_PATH")

settings = Settings()
