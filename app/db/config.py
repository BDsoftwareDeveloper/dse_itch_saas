# app/core/config.py

import os
# from pydantic import BaseSettings
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "DSE SaaS Gateway"
    PROJECT_DESCRIPTION: str = "SaaS app for managing DSE socket connections"
    API_V1_PREFIX: str = "/api/v1"

    # PostgreSQL
    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER", "localhost")
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "saiful")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "saiful123")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "saas_dse_db")
    SQLALCHEMY_DATABASE_URI: str = (
        f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:5432/{POSTGRES_DB}"
    )

    print(f'SQLALCHEMY_DATABASE_URI: {SQLALCHEMY_DATABASE_URI}')
    # JWT
    SECRET_KEY: str = os.getenv("SECRET_KEY", "supersecret")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 1 day

    # pgAdmin
    PGADMIN_DEFAULT_EMAIL: str = os.getenv("PGADMIN_DEFAULT_EMAIL", "admin@gmail.com")
    PGADMIN_DEFAULT_PASSWORD: str = os.getenv("PGADMIN_DEFAULT_PASSWORD", "admin123")

    class Config:
        case_sensitive = True


settings = Settings()
