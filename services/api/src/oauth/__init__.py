from src.oauth.base import OAuthProvider, OAuthProviderError
from src.oauth.google import GoogleOAuthAdapter
from src.oauth.microsoft import MicrosoftOAuthAdapter

_PROVIDERS: dict[str, OAuthProvider] = {
    "google": GoogleOAuthAdapter(),
    "microsoft": MicrosoftOAuthAdapter(),
}


def get_oauth_provider(name: str) -> OAuthProvider:
    provider = _PROVIDERS.get(name.lower())
    if not provider:
        raise OAuthProviderError(
            f"Unsupported OAuth provider: '{name}'. Supported providers: {list(_PROVIDERS.keys())}"
        )
    return provider


__all__ = [
    "OAuthProvider",
    "OAuthProviderError",
    "GoogleOAuthAdapter",
    "MicrosoftOAuthAdapter",
    "get_oauth_provider",
]
