from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    groq_api_key: str
    groq_chat_model: str = "qwen/qwen3.8-27b"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()