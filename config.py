from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    openai_api_key: str = ""
    anthropic_api_key: str = ""
    image_model: str = "dall-e-3"
    tts_model: str = "tts-1"
    text_model: str = "gpt-4"
    output_dir: str = "output"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
