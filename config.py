from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    qiniu_api_key: str = "sk-c4a3fc02a12d3a64727f6d55178bcc8c44356cb8544e7b2036b003f7c6d17297"
    qiniu_base_url: str = "https://openai.qiniu.com/v1"
    qiniu_backup_url: str = "https://api.qnaigc.com/v1"
    
    openai_api_key: str = ""
    anthropic_api_key: str = ""
    
    image_model: str = "gemini-2.5-flash-image"
    tts_voice_type: str = "qiniu_zh_female_wwxkjx"
    text_model: str = "gpt-3.5-turbo"
    output_dir: str = "output"
    
    web_host: str = "0.0.0.0"
    web_port: int = 8088
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


settings = Settings()
