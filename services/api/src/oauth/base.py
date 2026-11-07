from abc import ABC, abstractmethod
from typing import Any


class OAuthProviderError(Exception):
    """Raised when an error occurs in communication with an OAuth provider."""

    pass


def sanitize_sensitive_data(message: str, *secrets: str | None) -> str:
    """Ensure no secrets, refresh tokens, or client secrets leak into error strings."""
    sanitized = message
    for secret in secrets:
        if secret and len(secret) > 3:
            sanitized = sanitized.replace(secret, "[REDACTED]")
    return sanitized


class OAuthProvider(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        """Provider name, e.g. 'google' or 'microsoft'."""
        pass

    @property
    @abstractmethod
    def scopes(self) -> list[str]:
        """List of requested scopes (least privilege)."""
        pass

    @abstractmethod
    def get_authorization_url(self, state: str, code_challenge: str) -> str:
        """Generate provider consent URL with PKCE and state."""
        pass

    @abstractmethod
    async def exchange_code(self, code: str, code_verifier: str) -> dict[str, Any]:
        """Exchange authorization code and PKCE code_verifier for tokens.

        Returns dict containing:
        - access_token: str
        - refresh_token: Optional[str]
        - token_type: str
        - expires_in: int
        - scopes: List[str]
        - raw_response: Dict[str, Any]
        """
        pass

    @abstractmethod
    async def refresh_tokens(self, refresh_token: str) -> dict[str, Any]:
        """Use refresh token to obtain fresh access token."""
        pass

    @abstractmethod
    async def get_user_profile(self, access_token: str) -> dict[str, Any]:
        """Fetch user email and display name using provider access token.

        Returns dict containing:
        - email: str
        - display_name: Optional[str]
        """
        pass

    @abstractmethod
    async def revoke_token(self, token: str) -> bool:
        """Revoke the granted OAuth token with the provider."""
        pass
