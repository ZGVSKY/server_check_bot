from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr

class Settings(BaseSettings):
    bot_token: SecretStr
    admin_id: int
    temp_threshold: int = 80  # Поріг температури за замовчуванням
    
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

config = Settings()
