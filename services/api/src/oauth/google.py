import urllib.parse
from typing import Any

import httpx

from src.config import get_settings
from src.oauth.base import OAuthProvider, OAuthProviderError, sanitize_sensitive_data


class GoogleOAuthAdapter(OAuthProvider):
    AUTH_ENDPOINT = "https://accounts.google.com/o/oauth2/v2/auth"
    TOKEN_ENDPOINT = "https://oauth2.googleapis.com/token"
    USERINFO_ENDPOINT = "https://www.googleapis.com/oauth2/v2/userinfo"
    REVOKE_ENDPOINT = "https://oauth2.googleapis.com/revoke"

    @property
    def name(self) -> str:
        return "google"

    @property
    def scopes(self) -> list[str]:
        return [
            "openid",
            "https://www.googleapis.com/auth/userinfo.email",
            "https://www.googleapis.com/auth/userinfo.profile",
            "https://www.googleapis.com/auth/gmail.readonly",
        ]

    def get_authorization_url(self, state: str, code_challenge: str) -> str:
        settings = get_settings()
        params = {
            "client_id": settings.GOOGLE_CLIENT_ID,
            "redirect_uri": settings.GOOGLE_REDIRECT_URI,
            "response_type": "code",
            "scope": " ".join(self.scopes),
            "access_type": "offline",
            "prompt": "consent",
            "state": state,
            "code_challenge": code_challenge,
            "code_challenge_method": "S256",
        }
        return f"{self.AUTH_ENDPOINT}?{urllib.parse.urlencode(params)}"

    async def exchange_code(self, code: str, code_verifier: str) -> dict[str, Any]:
        settings = get_settings()
        payload = {
            "client_id": settings.GOOGLE_CLIENT_ID,
            "client_secret": settings.GOOGLE_CLIENT_SECRET,
            "code": code,
            "code_verifier": code_verifier,
            "grant_type": "authorization_code",
            "redirect_uri": settings.GOOGLE_REDIRECT_URI,
        }

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.post(self.TOKEN_ENDPOINT, data=payload)
                if resp.status_code != 200:
                    clean_msg = sanitize_sensitive_data(
                        resp.text,
                        settings.GOOGLE_CLIENT_SECRET,
                        code,
                        code_verifier,
                    )
                    raise OAuthProviderError(
                        f"Google token exchange failed with status {resp.status_code}: {clean_msg}"
                    )
                data = resp.json()
        except httpx.HTTPError as e:
            raise OAuthProviderError(f"HTTP error during Google token exchange: {e}") from e

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
        payload = {
            "client_id": settings.GOOGLE_CLIENT_ID,
            "client_secret": settings.GOOGLE_CLIENT_SECRET,
            "refresh_token": refresh_token,
            "grant_type": "refresh_token",
        }

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.post(self.TOKEN_ENDPOINT, data=payload)
                if resp.status_code != 200:
                    clean_msg = sanitize_sensitive_data(
                        resp.text,
                        settings.GOOGLE_CLIENT_SECRET,
                        refresh_token,
                    )
                    raise OAuthProviderError(
                        f"Google token refresh failed with status {resp.status_code}: {clean_msg}"
                    )
                data = resp.json()
        except httpx.HTTPError as e:
            raise OAuthProviderError(f"HTTP error during Google token refresh: {e}") from e

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
        headers = {"Authorization": f"Bearer {access_token}"}
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.get(self.USERINFO_ENDPOINT, headers=headers)
                if resp.status_code != 200:
                    raise OAuthProviderError(
                        f"Failed to fetch Google profile: {resp.status_code} {resp.text}"
                    )
                data = resp.json()
        except httpx.HTTPError as e:
            raise OAuthProviderError(f"HTTP error fetching Google profile: {e}") from e

        return {
            "email": data.get("email"),
            "display_name": data.get("name") or data.get("email"),
        }

    async def revoke_token(self, token: str) -> bool:
        """Revoke a token with Google OAuth."""
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.post(self.REVOKE_ENDPOINT, params={"token": token})
                return resp.status_code == 200
        except Exception:
            return False
