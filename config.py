from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    qiniu_api_key: str = ""
    qiniu_base_url: str = "https://openai.qiniu.com/v1"
    qiniu_backup_url: str = "https://api.qnaigc.com/v1"
    
    image_model: str = "gemini-2.5-flash-image"
    tts_voice_type: str = "qiniu_zh_female_wwxkjx"
    text_model: str = "gpt-3.5-turbo"
    output_dir: str = "output"
    
    web_host: str = "0.0.0.0"
    web_port: int = 5000
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


settings = Settings()
