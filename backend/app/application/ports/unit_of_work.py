from __future__ import annotations

from typing import Protocol


class UnitOfWork(Protocol):
    async def commit(self) -> None:
        """Commit the active transaction."""

    async def rollback(self) -> None:
        """Rollback the active transaction."""

