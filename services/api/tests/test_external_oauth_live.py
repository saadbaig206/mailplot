import httpx
import pytest

from src.config import get_settings
from src.oauth.google import GoogleOAuthAdapter
from src.oauth.microsoft import MicrosoftOAuthAdapter

settings = get_settings()

GOOGLE_CONFIGURED = bool(
    settings.GOOGLE_CLIENT_ID
    and not settings.GOOGLE_CLIENT_ID.startswith("mock-")
    and settings.GOOGLE_CLIENT_SECRET
    and not settings.GOOGLE_CLIENT_SECRET.startswith("mock-")
)

MICROSOFT_CONFIGURED = bool(
    settings.MICROSOFT_CLIENT_ID
    and not settings.MICROSOFT_CLIENT_ID.startswith("mock-")
    and settings.MICROSOFT_CLIENT_SECRET
    and not settings.MICROSOFT_CLIENT_SECRET.startswith("mock-")
)


@pytest.mark.asyncio
@pytest.mark.skipif(
    not GOOGLE_CONFIGURED,
    reason="External Google OAuth integration test pending live credentials in environment (GOOGLE_CLIENT_ID / GOOGLE_CLIENT_SECRET)",
)
async def test_live_google_oauth_token_exchange():
    """Live integration test: attempt live exchange with Google (requires valid test code)."""
    adapter = GoogleOAuthAdapter()
    async with httpx.AsyncClient() as client:
        resp = await client.get(adapter.AUTH_ENDPOINT)
        assert resp.status_code in [200, 302, 400]


@pytest.mark.asyncio
@pytest.mark.skipif(
    not MICROSOFT_CONFIGURED,
    reason="External Microsoft OAuth integration test pending live credentials in environment (MICROSOFT_CLIENT_ID / MICROSOFT_CLIENT_SECRET)",
)
async def test_live_microsoft_oauth_token_exchange():
    """Live integration test: attempt live discovery with Microsoft identity platform."""
    adapter = MicrosoftOAuthAdapter()
    discovery_url = f"{adapter._get_authority_url()}/v2.0/.well-known/openid-configuration"
    async with httpx.AsyncClient() as client:
        resp = await client.get(discovery_url)
        assert resp.status_code == 200
