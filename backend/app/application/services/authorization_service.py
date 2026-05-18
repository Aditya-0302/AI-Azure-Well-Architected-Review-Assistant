from __future__ import annotations

from app.core.exceptions import PermissionDeniedError
from app.core.security import Principal


class AuthorizationService:
    WRITE_PROJECT_ROLES = {"admin", "architect"}
    REVIEW_ROLES = {"admin", "architect", "reviewer"}
    READ_ROLES = {"admin", "architect", "reviewer", "manager"}

    def require_role(self, principal: Principal, allowed_roles: set[str]) -> None:
        if principal.is_admin:
            return
        if not allowed_roles.intersection(principal.roles):
            raise PermissionDeniedError()

    def require_project_write(self, principal: Principal) -> None:
        self.require_role(principal, self.WRITE_PROJECT_ROLES)

    def require_review_access(self, principal: Principal) -> None:
        self.require_role(principal, self.REVIEW_ROLES)

    def require_read_access(self, principal: Principal) -> None:
        self.require_role(principal, self.READ_ROLES)

