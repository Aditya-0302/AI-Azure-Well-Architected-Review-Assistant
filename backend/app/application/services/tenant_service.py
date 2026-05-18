from __future__ import annotations

from app.application.dto.tenants import TenantResponse
from app.core.config import Settings
from app.core.security import Principal


class TenantService:
    def __init__(self, settings: Settings) -> None:
        self._settings = settings

    async def get_current_tenant(self, principal: Principal) -> TenantResponse:
        tenant_id = principal.tenant_id or "unknown"
        return TenantResponse(
            id=tenant_id,
            name="Local Tenant" if tenant_id == "local-tenant" else tenant_id,
            slug=tenant_id.lower().replace("_", "-"),
            environment=self._settings.app_env,
        )

