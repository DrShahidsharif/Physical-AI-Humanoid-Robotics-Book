from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # OpenRouter configuration
    OPENROUTER_API_KEY: str
    OPENROUTER_BASE_URL: str = "https://openrouter.ai/api/v1"
    OPENROUTER_MODEL: str = "openchat/openchat-7b:free"  # Default model, can be changed

    # Qdrant configuration
    QDRANT_URL: str
    QDRANT_API_KEY: Optional[str] = None
    QDRANT_HOST: Optional[str] = None  # For local instances
    QDRANT_PORT: int = 6333

    # Neon Postgres configuration
    NEON_DATABASE_URL: str

    # Application settings
    APP_NAME: str = "RAG Book Chatbot"
    DEBUG: bool = False
    API_V1_STR: str = "/api/v1"

    class Config:
        env_file = ".env"


settings = Settings()