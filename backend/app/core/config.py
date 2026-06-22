from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/tms_db"

    # proper PostgreSQL URL derived from current local settings
    class Config:
        env_file = ".env"

settings = Settings()