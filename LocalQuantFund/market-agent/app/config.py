"""Configuration settings for market-agent."""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""
    
    class Config:
        env_file = ".env"


settings = Settings()
