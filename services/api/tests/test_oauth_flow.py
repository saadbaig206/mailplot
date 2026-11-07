import urllib.parse
from unittest.mock import AsyncMock, patch

import pytest
from httpx import AsyncClient

from src.oauth.base import OAuthProviderError
from src.oauth.google import GoogleOAuthAdapter


@pytest.mark.asyncio
async def test_oauth_start_google(async_client: AsyncClient, user_a_token: str):
    """Verify Google OAuth start endpoint returns proper consent URL and scopes."""
    headers = {"Authorization": f"Bearer {user_a_token}"}
    response = await async_client.get("/api/v1/oauth/google/start", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["provider"] == "google"
    auth_url = data["authorization_url"]

    # Verify query parameters in auth_url
    parsed = urllib.parse.urlparse(auth_url)
    params = urllib.parse.parse_qs(parsed.query)

    assert "client_id" in params
    assert "redirect_uri" in params
    assert "response_type" in params and params["response_type"][0] == "code"
    assert "code_challenge" in params
    assert "code_challenge_method" in params and params["code_challenge_method"][0] == "S256"
    assert "state" in params

    # Verify least-privilege read-only gmail scopes
    scope_str = params["scope"][0]
    assert "https://www.googleapis.com/auth/gmail.readonly" in scope_str
    assert "openid" in scope_str


@pytest.mark.asyncio
async def test_oauth_start_microsoft(async_client: AsyncClient, user_a_token: str):
    """Verify Microsoft OAuth start endpoint returns proper consent URL and delegated scopes."""
    headers = {"Authorization": f"Bearer {user_a_token}"}
    response = await async_client.get("/api/v1/oauth/microsoft/start", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["provider"] == "microsoft"
    auth_url = data["authorization_url"]

    parsed = urllib.parse.urlparse(auth_url)
    params = urllib.parse.parse_qs(parsed.query)

    assert "code_challenge" in params
    assert "code_challenge_method" in params and params["code_challenge_method"][0] == "S256"
    assert "state" in params

    # Verify least-privilege Mail.Read and offline_access
    scope_str = params["scope"][0]
    assert "Mail.Read" in scope_str
    assert "offline_access" in scope_str


@pytest.mark.asyncio
async def test_oauth_callback_success(async_client: AsyncClient, user_a_token: str):
    """Verify full OAuth callback flow for Google."""
    headers = {"Authorization": f"Bearer {user_a_token}"}

    # 1. Start OAuth
    start_resp = await async_client.get("/api/v1/oauth/google/start", headers=headers)
    assert start_resp.status_code == 200
    auth_url = start_resp.json()["authorization_url"]
    parsed = urllib.parse.urlparse(auth_url)
    state = urllib.parse.parse_qs(parsed.query)["state"][0]

    # 2. Mock token exchange and user info
    with (
        patch(
            "src.oauth.google.GoogleOAuthAdapter.exchange_code", new_callable=AsyncMock
        ) as mock_exchange,
        patch(
            "src.oauth.google.GoogleOAuthAdapter.get_user_profile", new_callable=AsyncMock
        ) as mock_profile,
    ):
        mock_exchange.return_value = {
            "access_token": "ya29.mock-google-access-token",
            "refresh_token": "1//mock-google-refresh-token",
            "token_type": "Bearer",
            "expires_in": 3600,
            "scopes": ["gmail.readonly"],
            "raw_response": {"token_id": "123"},
        }
        mock_profile.return_value = {
            "email": "executive@company.com",
            "display_name": "Executive Officer",
        }

        # 3. Post callback
        cb_resp = await async_client.post(
            "/api/v1/oauth/google/callback",
            headers=headers,
            json={"code": "sample-authorization-code", "state": state},
        )
        assert cb_resp.status_code == 200
        data = cb_resp.json()
        assert data["success"] is True
        assert data["account"]["email_address"] == "executive@company.com"
        assert data["account"]["status"] == "active"
        assert "gmail.readonly" in data["account"]["scopes"]
        # Ensure tokens are NEVER exposed in JSON response!
        assert "access_token" not in data["account"]
        assert "encrypted_access_token" not in data["account"]


@pytest.mark.asyncio
async def test_oauth_callback_state_mismatch(async_client: AsyncClient, user_a_token: str):
    """Callback with invalid or tampered state must return 400 Bad Request."""
    headers = {"Authorization": f"Bearer {user_a_token}"}
    cb_resp = await async_client.post(
        "/api/v1/oauth/google/callback",
        headers=headers,
        json={"code": "sample-code", "state": "tampered-or-invalid-state-string"},
    )
    assert cb_resp.status_code == 400
    assert "state" in cb_resp.json()["detail"].lower()


@pytest.mark.asyncio
async def test_oauth_callback_replay(async_client: AsyncClient, user_a_token: str):
    """Replaying the same OAuth state must return 400 Bad Request."""
    headers = {"Authorization": f"Bearer {user_a_token}"}

    start_resp = await async_client.get("/api/v1/oauth/google/start", headers=headers)
    auth_url = start_resp.json()["authorization_url"]
    state = urllib.parse.parse_qs(urllib.parse.urlparse(auth_url).query)["state"][0]

    with (
        patch(
            "src.oauth.google.GoogleOAuthAdapter.exchange_code", new_callable=AsyncMock
        ) as mock_exchange,
        patch(
            "src.oauth.google.GoogleOAuthAdapter.get_user_profile", new_callable=AsyncMock
        ) as mock_profile,
    ):
        mock_exchange.return_value = {
            "access_token": "token1",
            "refresh_token": "refresh1",
            "token_type": "Bearer",
            "expires_in": 3600,
            "scopes": [],
            "raw_response": {},
        }
        mock_profile.return_value = {"email": "test@domain.com", "display_name": "Test"}

        # First callback succeeds
        resp1 = await async_client.post(
            "/api/v1/oauth/google/callback",
            headers=headers,
            json={"code": "code1", "state": state},
        )
        assert resp1.status_code == 200

        # Second callback with same state must fail with 400 (replay detected)
        resp2 = await async_client.post(
            "/api/v1/oauth/google/callback",
            headers=headers,
            json={"code": "code2", "state": state},
        )
        assert resp2.status_code == 400
        assert "replay" in resp2.json()["detail"].lower()


@pytest.mark.asyncio
async def test_token_refresh_failure_handling():
    """Verify that provider token refresh failure raises OAuthProviderError."""
    adapter = GoogleOAuthAdapter()
    with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
        mock_post.return_value.status_code = 400
        mock_post.return_value.text = (
            '{"error": "invalid_grant", "error_description": "Token has been expired or revoked."}'
        )

        with pytest.raises(OAuthProviderError, match="Google token refresh failed"):
            await adapter.refresh_tokens("revoked-refresh-token")


@pytest.mark.asyncio
async def test_provider_tokens_are_encrypted_at_rest(
    async_client: AsyncClient,
    user_a_token: str,
):
    """Verify that OAuth access & refresh tokens are encrypted at rest in the database."""
    from sqlalchemy import select

    from src.models.oauth_connection import OAuthConnection
    from src.security.encryption import decrypt_token
    from tests.conftest import TestAsyncSessionLocal

    headers = {"Authorization": f"Bearer {user_a_token}"}
    start_resp = await async_client.get("/api/v1/oauth/google/start", headers=headers)
    auth_url = start_resp.json()["authorization_url"]
    state = urllib.parse.parse_qs(urllib.parse.urlparse(auth_url).query)["state"][0]

    raw_secret_access = "secret_plaintext_access_token_12345"
    raw_secret_refresh = "secret_plaintext_refresh_token_67890"

    with (
        patch(
            "src.oauth.google.GoogleOAuthAdapter.exchange_code", new_callable=AsyncMock
        ) as mock_exchange,
        patch(
            "src.oauth.google.GoogleOAuthAdapter.get_user_profile", new_callable=AsyncMock
        ) as mock_profile,
    ):
        mock_exchange.return_value = {
            "access_token": raw_secret_access,
            "refresh_token": raw_secret_refresh,
            "token_type": "Bearer",
            "expires_in": 3600,
            "scopes": ["gmail.readonly"],
            "raw_response": {},
        }
        mock_profile.return_value = {
            "email": "encrypted_test@company.com",
            "display_name": "Encryption Test",
        }

        cb_resp = await async_client.post(
            "/api/v1/oauth/google/callback",
            headers=headers,
            json={"code": "auth-code", "state": state},
        )
        assert cb_resp.status_code == 200

    # Inspect the raw row in the database
    async with TestAsyncSessionLocal() as session:
        stmt = select(OAuthConnection)
        result = await session.execute(stmt)
        conn = result.scalar_one_or_none()
        assert conn is not None

        # 1. Stored tokens must NOT equal raw tokens
        assert conn.encrypted_access_token != raw_secret_access
        assert conn.encrypted_refresh_token != raw_secret_refresh

        # 2. Raw tokens must NOT be anywhere inside the ciphertext
        assert raw_secret_access not in conn.encrypted_access_token
        assert raw_secret_refresh not in conn.encrypted_refresh_token

        # 3. Decrypting ciphertext recovers the exact original token
        assert decrypt_token(conn.encrypted_access_token) == raw_secret_access
        assert decrypt_token(conn.encrypted_refresh_token) == raw_secret_refresh


@pytest.mark.asyncio
async def test_token_refresh_failure_does_not_expose_secrets():
    """Verify that OAuth refresh error messages redact secrets and do not leak them."""
    from src.config import get_settings

    settings = get_settings()
    adapter = GoogleOAuthAdapter()
    secret_refresh_token = "secret-refresh-token-xyz-12345"

    with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
        mock_post.return_value.status_code = 400
        # Simulate provider echoing back part of client secret or refresh token in error body
        mock_post.return_value.text = (
            f'{{"error": "invalid_grant", "reflected_secret": "{settings.GOOGLE_CLIENT_SECRET}", '
            f'"reflected_token": "{secret_refresh_token}"}}'
        )

        with pytest.raises(OAuthProviderError) as exc_info:
            await adapter.refresh_tokens(secret_refresh_token)

        err_str = str(exc_info.value)
        # Verify secrets are redacted and do NOT appear in the exception message
        assert settings.GOOGLE_CLIENT_SECRET not in err_str
        assert secret_refresh_token not in err_str
        assert "[REDACTED]" in err_str


@pytest.mark.asyncio
async def test_disconnect_mailbox_invalidates_local_connection(
    async_client: AsyncClient,
    user_a_token: str,
):
    """Verify disconnecting an email account permanently invalidates the connection."""
    headers = {"Authorization": f"Bearer {user_a_token}"}
    start_resp = await async_client.get("/api/v1/oauth/google/start", headers=headers)
    auth_url = start_resp.json()["authorization_url"]
    state = urllib.parse.parse_qs(urllib.parse.urlparse(auth_url).query)["state"][0]

    with (
        patch(
            "src.oauth.google.GoogleOAuthAdapter.exchange_code", new_callable=AsyncMock
        ) as mock_exchange,
        patch(
            "src.oauth.google.GoogleOAuthAdapter.get_user_profile", new_callable=AsyncMock
        ) as mock_profile,
    ):
        mock_exchange.return_value = {
            "access_token": "token-to-delete",
            "refresh_token": "refresh-to-delete",
            "token_type": "Bearer",
            "expires_in": 3600,
            "scopes": ["gmail.readonly"],
            "raw_response": {},
        }
        mock_profile.return_value = {
            "email": "to_disconnect@example.com",
            "display_name": "To Disconnect",
        }

        cb_resp = await async_client.post(
            "/api/v1/oauth/google/callback",
            headers=headers,
            json={"code": "code", "state": state},
        )
        assert cb_resp.status_code == 200
        account_id = cb_resp.json()["account"]["id"]

    # Verify mailbox is active
    accounts_before = await async_client.get("/api/v1/email-accounts", headers=headers)
    assert any(a["id"] == account_id for a in accounts_before.json())

    # Disconnect
    with patch(
        "src.oauth.google.GoogleOAuthAdapter.revoke_token", new_callable=AsyncMock
    ) as mock_revoke:
        mock_revoke.return_value = True
        del_resp = await async_client.delete(
            f"/api/v1/email-accounts/{account_id}", headers=headers
        )
        assert del_resp.status_code == 200
        assert del_resp.json()["success"] is True

    # Verify mailbox is completely removed / invalidated
    accounts_after = await async_client.get("/api/v1/email-accounts", headers=headers)
    assert not any(a["id"] == account_id for a in accounts_after.json())

    # Further disconnect attempts must return 404
    second_del = await async_client.delete(f"/api/v1/email-accounts/{account_id}", headers=headers)
    assert second_del.status_code == 404
