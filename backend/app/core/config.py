"""
Sports EL — Application Configuration
Reads all settings from environment variables / .env file.
"""
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    # Application
    APP_NAME: str = "Sports EL"
    APP_ENV: str = "development"
    APP_DEBUG: bool = True
    APP_PORT: int = 8000
    APP_SECRET_KEY: str = "change-me"

    # Database
    DATABASE_URL: str = "postgresql+asyncpg://postgres:password@localhost:5432/sports_el"

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # JWT
    JWT_SECRET_KEY: str = "change-me-jwt"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = 30

    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:5173"]

    # Signal Processing Defaults
    DEFAULT_SAMPLING_RATE_HZ: int = 100
    DEFAULT_WINDOW_SIZE_SEC: float = 5.0
    DEFAULT_WINDOW_OVERLAP: float = 0.5
    DEFAULT_FILTER_CUTOFF_HZ: float = 20.0
    DEFAULT_FILTER_ORDER: int = 4
    ARTIFACT_THRESHOLD_SIGMA: float = 5.0
    ENTROPY_M_PARAM: int = 2
    ENTROPY_R_FACTOR: float = 0.2

    # Fatigue Thresholds
    FATIGUE_THRESHOLD_EARLY: float = 20.0
    FATIGUE_THRESHOLD_MODERATE: float = 40.0
    FATIGUE_THRESHOLD_HIGH: float = 65.0

    # Logging
    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


settings = Settings()
