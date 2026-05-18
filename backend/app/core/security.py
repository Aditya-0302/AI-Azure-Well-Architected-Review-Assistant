from __future__ import annotations

from datetime import UTC, datetime
from functools import cached_property

import jwt
from jwt import PyJWKClient
from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.core.config import AppEnvironment, Settings
from app.core.exceptions import AuthenticationError, DependencyUnavailableError


class Principal(BaseModel):
    model_config = ConfigDict(frozen=True)

    subject: str
    tenant_id: str | None = None
    email: EmailStr | None = None
    display_name: str | None = None
    roles: frozenset[str] = Field(default_factory=frozenset)
    scopes: frozenset[str] = Field(default_factory=frozenset)
    entra_object_id: str | None = None
    issued_at: datetime | None = None

    def has_role(self, *required: str) -> bool:
        return bool(set(required).intersection(self.roles))

    def has_scope(self, *required: str) -> bool:
        return bool(set(required).intersection(self.scopes))

    @property
    def is_admin(self) -> bool:
        return "admin" in self.roles


class TokenValidator:
    def __init__(self, settings: Settings) -> None:
        self._settings = settings

    @cached_property
    def _jwks_client(self) -> PyJWKClient:
        jwks_url = self._settings.resolved_jwks_url
        if not jwks_url:
            raise DependencyUnavailableError(
                "AUTH_JWKS_URL or AUTH_TENANT_ID must be configured for Entra ID auth.",
                code="auth_jwks_not_configured",
            )
        return PyJWKClient(jwks_url)

    async def validate(self, token: str) -> Principal:
        if self._settings.auth_mode == "local":
            return self._validate_local_token(token)
        return self._validate_entra_token(token)

    def _validate_local_token(self, token: str) -> Principal:
        if (
            self._settings.app_env != AppEnvironment.LOCAL
            or not self._settings.auth_allow_local_tokens
        ):
            raise AuthenticationError("Local development tokens are disabled.")

        parts = token.split(":", maxsplit=2)
        if len(parts) != 3 or parts[0] != "local":
            raise AuthenticationError("Invalid local token format.")

        email = parts[1]
        roles = frozenset(role.strip() for role in parts[2].split(",") if role.strip())
        if not roles:
            roles = frozenset({"architect"})

        return Principal(
            subject=email,
            tenant_id="local-tenant",
            email=email,
            display_name=email,
            roles=roles,
            scopes=frozenset({"local"}),
            entra_object_id=None,
            issued_at=datetime.now(UTC),
        )

    def _validate_entra_token(self, token: str) -> Principal:
        issuer = self._settings.resolved_auth_issuer
        if not issuer:
            raise DependencyUnavailableError(
                "AUTH_ISSUER or AUTH_TENANT_ID must be configured for Entra ID auth.",
                code="auth_issuer_not_configured",
            )

        try:
            signing_key = self._jwks_client.get_signing_key_from_jwt(token)
            payload = jwt.decode(
                token,
                signing_key.key,
                algorithms=["RS256"],
                audience=self._settings.auth_audience,
                issuer=issuer,
                options={"require": ["exp", "iat"]},
            )
        except jwt.PyJWTError as exc:
            raise AuthenticationError("Invalid bearer token.") from exc

        scopes = frozenset(str(payload.get("scp", "")).split())
        roles = frozenset(payload.get("roles", []) or [])
        email = payload.get("preferred_username") or payload.get("email") or payload.get("upn")

        return Principal(
            subject=str(payload.get("sub")),
            tenant_id=payload.get("tid"),
            email=email,
            display_name=payload.get("name"),
            roles=roles,
            scopes=scopes,
            entra_object_id=payload.get("oid"),
            issued_at=datetime.fromtimestamp(int(payload["iat"]), tz=UTC),
        )

