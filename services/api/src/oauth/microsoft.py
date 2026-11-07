import urllib.parse
from typing import Any

import httpx

from src.config import get_settings
from src.oauth.base import OAuthProvider, OAuthProviderError, sanitize_sensitive_data


class MicrosoftOAuthAdapter(OAuthProvider):
    @property
    def name(self) -> str:
        return "microsoft"

    @property
    def scopes(self) -> list[str]:
        return [
            "openid",
            "profile",
            "email",
            "offline_access",
            "Mail.Read",
        ]

    def _get_authority_url(self) -> str:
        settings = get_settings()
        tenant = settings.MICROSOFT_TENANT_ID or "common"
        return f"https://login.microsoftonline.com/{tenant}/oauth2/v2.0"

    def get_authorization_url(self, state: str, code_challenge: str) -> str:
        settings = get_settings()
        params = {
            "client_id": settings.MICROSOFT_CLIENT_ID,
            "response_type": "code",
            "redirect_uri": settings.MICROSOFT_REDIRECT_URI,
            "response_mode": "query",
            "scope": " ".join(self.scopes),
            "state": state,
            "code_challenge": code_challenge,
            "code_challenge_method": "S256",
            "prompt": "select_account",
        }
        endpoint = f"{self._get_authority_url()}/authorize"
        return f"{endpoint}?{urllib.parse.urlencode(params)}"

    async def exchange_code(self, code: str, code_verifier: str) -> dict[str, Any]:
        settings = get_settings()
        endpoint = f"{self._get_authority_url()}/token"
        payload = {
            "client_id": settings.MICROSOFT_CLIENT_ID,
            "client_secret": settings.MICROSOFT_CLIENT_SECRET,
            "code": code,
            "code_verifier": code_verifier,
            "grant_type": "authorization_code",
            "redirect_uri": settings.MICROSOFT_REDIRECT_URI,
            "scope": " ".join(self.scopes),
        }

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.post(endpoint, data=payload)
                if resp.status_code != 200:
                    clean_msg = sanitize_sensitive_data(
                        resp.text,
                        settings.MICROSOFT_CLIENT_SECRET,
                        code,
                        code_verifier,
                    )
                    raise OAuthProviderError(
                        f"Microsoft token exchange failed with status {resp.status_code}: {clean_msg}"
                    )
                data = resp.json()
        except httpx.HTTPError as e:
            raise OAuthProviderError(f"HTTP error during Microsoft token exchange: {e}") from e

        return {
            "access_token": data.get("access_token"),
            "refresh_token": data.get("refresh_token"),
            "token_type": data.get("token_type", "Bearer"),
            "expires_in": data.get("expires_in", 3600),
            "scopes": data.get("scope", "").split(" ") if data.get("scope") else self.scopes,
            "raw_response": {
                k: v for k, v in data.items() if k not in ["access_token", "refresh_token"]
            },
        }

    async def refresh_tokens(self, refresh_token: str) -> dict[str, Any]:
        settings = get_settings()
        endpoint = f"{self._get_authority_url()}/token"
        payload = {
            "client_id": settings.MICROSOFT_CLIENT_ID,
            "client_secret": settings.MICROSOFT_CLIENT_SECRET,
            "refresh_token": refresh_token,
            "grant_type": "refresh_token",
            "scope": " ".join(self.scopes),
        }

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.post(endpoint, data=payload)
                if resp.status_code != 200:
                    clean_msg = sanitize_sensitive_data(
                        resp.text,
                        settings.MICROSOFT_CLIENT_SECRET,
                        refresh_token,
                    )
                    raise OAuthProviderError(
                        f"Microsoft token refresh failed with status {resp.status_code}: {clean_msg}"
                    )
                data = resp.json()
        except httpx.HTTPError as e:
            raise OAuthProviderError(f"HTTP error during Microsoft token refresh: {e}") from e

        return {
            "access_token": data.get("access_token"),
            "refresh_token": data.get("refresh_token", refresh_token),
            "token_type": data.get("token_type", "Bearer"),
            "expires_in": data.get("expires_in", 3600),
            "scopes": data.get("scope", "").split(" ") if data.get("scope") else self.scopes,
            "raw_response": {
                k: v for k, v in data.items() if k not in ["access_token", "refresh_token"]
            },
        }

    async def get_user_profile(self, access_token: str) -> dict[str, Any]:
        endpoint = "https://graph.microsoft.com/v1.0/me"
        headers = {"Authorization": f"Bearer {access_token}"}
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.get(endpoint, headers=headers)
                if resp.status_code != 200:
                    raise OAuthProviderError(
                        f"Failed to fetch Microsoft profile: {resp.status_code} {resp.text}"
                    )
                data = resp.json()
        except httpx.HTTPError as e:
            raise OAuthProviderError(f"HTTP error fetching Microsoft profile: {e}") from e

        email = data.get("mail") or data.get("userPrincipalName")
        return {
            "email": email,
            "display_name": data.get("displayName") or email,
        }

    async def revoke_token(self, token: str) -> bool:
        """Microsoft does not expose an open revocation endpoint for delegated tokens;
        connections are invalidated by deleting the server-side token record.
        """
        return True
