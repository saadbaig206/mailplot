from unittest.mock import AsyncMock, patch

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_tenant_isolation_cross_user_denial(
    async_client: AsyncClient,
    user_a_token: str,
    user_b_token: str,
):
    """Verify that User B cannot view, modify, or disconnect User A's email accounts."""
    headers_a = {"Authorization": f"Bearer {user_a_token}"}
    headers_b = {"Authorization": f"Bearer {user_b_token}"}

    # 1. User A initiates and connects a mock Google mailbox
    with (
        patch(
            "src.oauth.google.GoogleOAuthAdapter.exchange_code", new_callable=AsyncMock
        ) as mock_exchange,
        patch(
            "src.oauth.google.GoogleOAuthAdapter.get_user_profile", new_callable=AsyncMock
        ) as mock_profile,
    ):
        mock_exchange.return_value = {
            "access_token": "mock-user-a-access-token",
            "refresh_token": "mock-user-a-refresh-token",
            "token_type": "Bearer",
            "expires_in": 3600,
            "scopes": ["gmail.readonly"],
            "raw_response": {},
        }
        mock_profile.return_value = {
            "email": "user_a_mailbox@gmail.com",
            "display_name": "User A Mailbox",
        }

        # Start OAuth for User A to get state
        start_resp = await async_client.get("/api/v1/oauth/google/start", headers=headers_a)
        assert start_resp.status_code == 200
        auth_url = start_resp.json()["authorization_url"]

        # Extract state from URL
        import urllib.parse

        parsed = urllib.parse.urlparse(auth_url)
        params = urllib.parse.parse_qs(parsed.query)
        state = params["state"][0]

        # User A completes callback
        cb_resp = await async_client.post(
            "/api/v1/oauth/google/callback",
            headers=headers_a,
            json={"code": "valid-auth-code", "state": state},
        )
        assert cb_resp.status_code == 200
        account_a_id = cb_resp.json()["account"]["id"]

    # 2. User A sees their connected account
    list_a = await async_client.get("/api/v1/email-accounts", headers=headers_a)
    assert list_a.status_code == 200
    accounts_a = list_a.json()
    assert len(accounts_a) == 1
    assert accounts_a[0]["id"] == account_a_id

    # 3. User B calls GET /api/v1/email-accounts -> must be empty (tenant isolation)
    list_b = await async_client.get("/api/v1/email-accounts", headers=headers_b)
    assert list_b.status_code == 200
    accounts_b = list_b.json()
    assert len(accounts_b) == 0

    # 4. User B attempts to DELETE User A's email account -> must return 404
    del_resp_b = await async_client.delete(
        f"/api/v1/email-accounts/{account_a_id}", headers=headers_b
    )
    assert del_resp_b.status_code == 404
    assert "not found" in del_resp_b.json()["detail"].lower()

    # 5. User A deletes their own email account -> must succeed with 200
    with patch(
        "src.oauth.google.GoogleOAuthAdapter.revoke_token", new_callable=AsyncMock
    ) as mock_revoke:
        mock_revoke.return_value = True
        del_resp_a = await async_client.delete(
            f"/api/v1/email-accounts/{account_a_id}", headers=headers_a
        )
        assert del_resp_a.status_code == 200
        assert del_resp_a.json()["success"] is True

    # 6. Verify account is gone for User A as well
    list_a_after = await async_client.get("/api/v1/email-accounts", headers=headers_a)
    assert len(list_a_after.json()) == 0
