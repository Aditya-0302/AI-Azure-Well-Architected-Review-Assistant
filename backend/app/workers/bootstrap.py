from __future__ import annotations

from app.core.config import Settings, get_settings
from app.core.logging import configure_logging


def bootstrap_worker(settings: Settings | None = None) -> Settings:
    resolved = settings or get_settings()
    configure_logging(resolved)
    return resolved

