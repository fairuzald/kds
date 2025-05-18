import json
import secrets
from typing import Any, List, Optional

from pydantic import AnyHttpUrl, Field, field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "Bacteria Classification API"
    API_STR: str = "/api"
    ENVIRONMENT: str = "development"
    SECRET_KEY: str = secrets.token_urlsafe(32)

    CORS_ORIGINS: List[AnyHttpUrl] = Field(default_factory=list)

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Any) -> Any:
        """
        Handles parsing of CORS_ORIGINS from environment variables.
        Accepts a comma-separated string or a JSON string list.
        Returns a list of strings for Pydantic to validate as AnyHttpUrl.
        """
        if v is None:
            return []
        if isinstance(v, list):
            return [str(item) for item in v]
        if isinstance(v, str):
            if not v.strip():
                return []
            if v.startswith("[") and v.endswith("]"):
                try:
                    parsed_list = json.loads(v)
                    if isinstance(parsed_list, list):
                        return [str(item) for item in parsed_list]
                except json.JSONDecodeError:
                    pass
            return [origin.strip() for origin in v.split(",") if origin.strip()]

        return []

    POSTGRES_SERVER: str = "postgres"
    POSTGRES_USER: str = "bacterial_user"
    POSTGRES_PASSWORD: str = "password"
    POSTGRES_DB: str = "bacterial_classification"
    POSTGRES_PORT: str = "5432"
    DATABASE_URL: Optional[str] = None

    @model_validator(mode="before")
    @classmethod
    def assemble_db_connection_v2(cls, data: Any) -> Any:
        if isinstance(data, dict) and data.get("DATABASE_URL") is None:
            pg_user = data.get("POSTGRES_USER")
            pg_password = data.get("POSTGRES_PASSWORD")
            pg_server = data.get("POSTGRES_SERVER")
            pg_port = data.get("POSTGRES_PORT")
            pg_db = data.get("POSTGRES_DB")

            if all([pg_user, pg_password, pg_server, pg_port, pg_db]):
                data["DATABASE_URL"] = (
                    f"postgresql+psycopg2://{pg_user}:{pg_password}@"
                    f"{pg_server}:{pg_port}/{pg_db}"
                )
        return data

    ML_MODEL_PATH: str = "ml_models/bacteria_classifier_xgboost_with_smote_tuned.pkl"
    ML_MODEL_PRELOAD: bool = True
    LOG_LEVEL: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=True,
    )


settings = Settings()
