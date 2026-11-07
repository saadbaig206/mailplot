import time
from typing import Any

import httpx
import jwt
from jwt.algorithms import RSAAlgorithm

from src.config import get_settings


class OIDCValidationError(Exception):
    """Raised when OIDC token validation fails."""

    pass


class OIDCValidator:
    def __init__(self):
        self.settings = get_settings()
        self._jwks_cache: dict[str, Any] | None = None
        self._jwks_cache_expiry: float = 0
        self._cache_ttl_seconds: int = 3600  # 1 hour
        self._mock_jwks: dict[str, Any] | None = None

    async def get_jwks(self) -> dict[str, Any]:
        """Fetch and cache the JWKS from the managed OIDC provider."""
        if self._mock_jwks is not None:
            return self._mock_jwks

        now = time.time()
        if self._jwks_cache and now < self._jwks_cache_expiry:
            return self._jwks_cache

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.get(self.settings.OIDC_JWKS_URI)
                resp.raise_for_status()
                data = resp.json()
                self._jwks_cache = data
                self._jwks_cache_expiry = now + self._cache_ttl_seconds
                return data
        except Exception as e:
            if self._jwks_cache:
                return self._jwks_cache
            raise OIDCValidationError(
                f"Failed to fetch JWKS from {self.settings.OIDC_JWKS_URI}: {e}"
            ) from e

    def set_jwks_cache_for_testing(self, jwks: dict[str, Any]) -> None:
        """Inject a JWKS cache directly for unit tests."""
        self._mock_jwks = jwks
        self._jwks_cache = jwks
        self._jwks_cache_expiry = time.time() + 360000

    async def validate_token(self, token: str) -> dict[str, Any]:
        """Validate an OIDC JWT access token against the provider's JWKS.

        Validates:
        - Header structure (RS256, kid)
        - RSA signature against JWKS
        - Issuer (iss)
        - Audience (aud)
        - Expiration (exp)
        - Subject (sub)
        """
        if not token:
            raise OIDCValidationError("Missing authentication token")

        try:
            unverified_header = jwt.get_unverified_header(token)
        except Exception as e:
            raise OIDCValidationError(f"Invalid token format or header: {e}") from e

        alg = unverified_header.get("alg")
        if alg not in ["RS256", "HS256"]:
            raise OIDCValidationError(f"Unsupported token algorithm: {alg}")

        # Check if dev mock auth is allowed and token was signed with secret key (HS256)
        if alg == "HS256":
            if not self.settings.ENABLE_DEV_MOCK_AUTH:
                raise OIDCValidationError(
                    "Symmetric token signing not permitted in this environment"
                )
            try:
                payload = jwt.decode(
                    token,
                    self.settings.SECRET_KEY,
                    algorithms=["HS256"],
                    audience=self.settings.OIDC_AUDIENCE,
                    issuer=self.settings.OIDC_ISSUER,
                )
                return payload
            except jwt.ExpiredSignatureError as e:
                raise OIDCValidationError("Token has expired") from e
            except jwt.InvalidTokenError as e:
                raise OIDCValidationError(f"Invalid token: {e}") from e

        # Standard RS256 JWKS verification
        kid = unverified_header.get("kid")
        if not kid:
            raise OIDCValidationError("Token header is missing 'kid'")

        jwks = await self.get_jwks()
        keys = jwks.get("keys", [])
        key_dict = next((k for k in keys if k.get("kid") == kid), None)

        if not key_dict:
            # Force cache refresh and retry once
            self._jwks_cache = None
            jwks = await self.get_jwks()
            keys = jwks.get("keys", [])
            key_dict = next((k for k in keys if k.get("kid") == kid), None)

        if not key_dict:
            raise OIDCValidationError(f"No matching key found in JWKS for kid: {kid}")

        try:
            public_key = RSAAlgorithm.from_jwk(key_dict)
            payload = jwt.decode(
                token,
                public_key,
                algorithms=["RS256"],
                audience=self.settings.OIDC_AUDIENCE,
                issuer=self.settings.OIDC_ISSUER,
                options={"require": ["exp", "iss", "aud", "sub"]},
            )
            return payload
        except jwt.ExpiredSignatureError as e:
            raise OIDCValidationError("Token has expired") from e
        except jwt.InvalidIssuerError as e:
            raise OIDCValidationError("Invalid token issuer") from e
        except jwt.InvalidAudienceError as e:
            raise OIDCValidationError("Invalid token audience") from e
        except jwt.InvalidSignatureError as e:
            raise OIDCValidationError("Invalid token signature") from e
        except jwt.InvalidTokenError as e:
            raise OIDCValidationError(f"Invalid token: {e}") from e


# Singleton validator instance
oidc_validator = OIDCValidator()
