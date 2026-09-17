from pydantic import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "Stock Analytics API"

settings = Settings()
