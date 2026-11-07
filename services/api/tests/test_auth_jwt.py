import pytest
from httpx import AsyncClient

from tests.conftest import create_test_jwt


@pytest.mark.asyncio
async def test_unauthorized_access_missing_token(async_client: AsyncClient):
    """Missing Authorization header must return 401 Unauthorized."""
    response = await async_client.get("/api/v1/me")
    assert response.status_code == 401
    assert "detail" in response.json()


@pytest.mark.asyncio
async def test_invalid_jwt_malformed(async_client: AsyncClient):
    """Malformed JWT string must return 401 Unauthorized."""
    headers = {"Authorization": "Bearer not-a-valid-jwt-token"}
    response = await async_client.get("/api/v1/me", headers=headers)
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_invalid_jwt_tampered_signature(async_client: AsyncClient):
    """Tampered JWT signature must fail cryptographic verification with 401."""
    tampered_token = create_test_jwt(tamper_signature=True)
    headers = {"Authorization": f"Bearer {tampered_token}"}
    response = await async_client.get("/api/v1/me", headers=headers)
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_expired_jwt(async_client: AsyncClient):
    """Expired JWT must return 401 Unauthorized."""
    expired_token = create_test_jwt(expires_in_seconds=-300)
    headers = {"Authorization": f"Bearer {expired_token}"}
    response = await async_client.get("/api/v1/me", headers=headers)
    assert response.status_code == 401
    detail = response.json()["detail"].lower()
    assert "expired" in detail or "invalid" in detail


@pytest.mark.asyncio
async def test_invalid_issuer(async_client: AsyncClient):
    """JWT with mismatched issuer claim must return 401 Unauthorized."""
    wrong_issuer_token = create_test_jwt(issuer="https://malicious-idp.com/")
    headers = {"Authorization": f"Bearer {wrong_issuer_token}"}
    response = await async_client.get("/api/v1/me", headers=headers)
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_invalid_audience(async_client: AsyncClient):
    """JWT with mismatched audience claim must return 401 Unauthorized."""
    wrong_aud_token = create_test_jwt(audience="wrong-audience")
    headers = {"Authorization": f"Bearer {wrong_aud_token}"}
    response = await async_client.get("/api/v1/me", headers=headers)
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_valid_authenticated_request(async_client: AsyncClient, user_a_token: str):
    """Valid signed token must return 200 OK and provision/return user profile."""
    headers = {"Authorization": f"Bearer {user_a_token}"}
    response = await async_client.get("/api/v1/me", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "user_a@example.com"
    assert data["full_name"] == "User A"
    assert data["is_active"] is True
    assert "id" in data
    assert isinstance(data["email_accounts"], list)
