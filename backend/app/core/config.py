from __future__ import annotations

from enum import StrEnum
from functools import lru_cache
from typing import Any

from pydantic import Field, SecretStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppEnvironment(StrEnum):
    LOCAL = "local"
    DEV = "dev"
    TEST = "test"
    STAGE = "stage"
    PROD = "prod"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    app_name: str = "AI Azure Well-Architected Review Assistant API"
    app_version: str = "0.1.0"
    app_env: AppEnvironment = AppEnvironment.LOCAL
    debug: bool = False
    expose_docs: bool = True
    api_prefix: str = "/api/v1"
    public_api_base_url: str = "http://localhost:8000"

    log_level: str = "INFO"
    log_json: bool = True

    auth_mode: str = "local"
    auth_tenant_id: str | None = None
    auth_issuer: str | None = None
    auth_audience: str = "api://ai-azure-waf-review-assistant"
    auth_jwks_url: str | None = None
    auth_allow_local_tokens: bool = True
    auth_jwks_cache_ttl_seconds: int = 3600

    cors_origins: list[str] = Field(default_factory=lambda: ["http://localhost:3000"])
    trusted_hosts: list[str] = Field(default_factory=lambda: ["localhost", "127.0.0.1"])

    database_url: SecretStr = SecretStr(
        "postgresql+asyncpg://postgres:postgres@localhost:5432/waf_reviews"
    )
    db_pool_size: int = 10
    db_max_overflow: int = 20
    db_echo: bool = False

    redis_url: str = "redis://localhost:6379/0"
    rate_limit_enabled: bool = True
    rate_limit_requests_per_minute: int = 120

    azure_openai_endpoint: str | None = None
    azure_openai_api_version: str = "2024-10-21"
    azure_openai_chat_deployment: str = "gpt-4o"
    azure_openai_embedding_deployment: str = "text-embedding-3-large"

    azure_search_endpoint: str | None = None
    azure_search_index_prefix: str = "waf"

    azure_storage_account_url: str | None = None
    azure_storage_container_raw: str = "raw"
    azure_storage_container_normalized: str = "normalized"
    azure_storage_container_reports: str = "reports"

    azure_service_bus_fully_qualified_namespace: str | None = None
    service_bus_ingestion_queue: str = "ingestion-jobs"
    service_bus_review_queue: str = "review-jobs"
    service_bus_report_queue: str = "report-jobs"

    enable_open_telemetry: bool = True

    @field_validator("cors_origins", "trusted_hosts", mode="before")
    @classmethod
    def parse_csv_list(cls, value: Any) -> list[str]:
        if value is None:
            return []
        if isinstance(value, str):
            return [item.strip() for item in value.split(",") if item.strip()]
        if isinstance(value, list):
            return value
        raise TypeError("Expected a comma-separated string or list")

    @field_validator("auth_mode")
    @classmethod
    def validate_auth_mode(cls, value: str) -> str:
        value = value.lower().strip()
        if value not in {"local", "entra"}:
            raise ValueError("AUTH_MODE must be either 'local' or 'entra'")
        return value

    @property
    def resolved_auth_issuer(self) -> str | None:
        if self.auth_issuer:
            return self.auth_issuer
        if self.auth_tenant_id:
            return f"https://login.microsoftonline.com/{self.auth_tenant_id}/v2.0"
        return None

    @property
    def resolved_jwks_url(self) -> str | None:
        if self.auth_jwks_url:
            return self.auth_jwks_url
        if self.auth_tenant_id:
            return f"https://login.microsoftonline.com/{self.auth_tenant_id}/discovery/v2.0/keys"
        return None


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()

