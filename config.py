from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # OpenAI API配置
    openai_api_key: str = ""
    anthropic_api_key: str = ""
    
    # 七牛云API配置
    qiniu_api_key: str = ""
    qiniu_base_url: str = "https://openai.qiniu.com/v1"
    qiniu_backup_url: str = "https://api.qnaigc.com/v1"
    
    # 模型配置
    image_model: str = "dall-e-3"
    tts_model: str = "tts-1"
    text_model: str = "gpt-4"
    
    # 输出目录
    output_dir: str = "output"
    
    # Web服务配置
    web_host: str = "0.0.0.0"
    web_port: int = 5000
    web_debug: bool = False
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
