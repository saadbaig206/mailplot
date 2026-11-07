import json
import time
from collections.abc import AsyncGenerator

import jwt
import pytest_asyncio
from cryptography.hazmat.primitives.asymmetric import rsa
from httpx import ASGITransport, AsyncClient
from jwt.algorithms import RSAAlgorithm
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.config import get_settings
from src.database import get_db
from src.main import app
from src.models import Base
from src.security.oidc_validator import oidc_validator
from src.security.state_signer import reset_consumed_states_for_testing

# Generate an in-memory RSA keypair for testing RS256 tokens
_test_private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
)
_test_public_key = _test_private_key.public_key()
_test_kid = "test-key-id-1"

# Convert public key to JWK
_test_jwk = json.loads(RSAAlgorithm.to_jwk(_test_public_key))
_test_jwk["kid"] = _test_kid
_test_jwk["use"] = "sig"
_test_jwk["alg"] = "RS256"

TEST_JWKS = {"keys": [_test_jwk]}

# File-backed SQLite test database for clean cross-connection table visibility
TEST_DATABASE_URL = "sqlite+aiosqlite:///./test_runner.db"
test_engine = create_async_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
)
TestAsyncSessionLocal = async_sessionmaker(
    bind=test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


def create_test_jwt(
    sub: str = "test-user-123",
    email: str = "testuser@example.com",
    name: str = "Test User",
    expires_in_seconds: int = 3600,
    issuer: str = None,
    audience: str = None,
    kid: str = _test_kid,
    tamper_signature: bool = False,
) -> str:
    """Helper to generate cryptographically signed RS256 JWTs for testing."""
    settings = get_settings()
    now = int(time.time())
    payload = {
        "sub": sub,
        "email": email,
        "name": name,
        "iss": issuer or settings.OIDC_ISSUER,
        "aud": audience or settings.OIDC_AUDIENCE,
        "iat": now,
        "exp": now + expires_in_seconds,
    }
    headers = {"kid": kid}
    token = jwt.encode(payload, _test_private_key, algorithm="RS256", headers=headers)
    if tamper_signature:
        # Flip characters in the signature segment
        parts = token.split(".")
        tampered_sig = parts[2][:-4] + "XXXX"
        return f"{parts[0]}.{parts[1]}.{tampered_sig}"
    return token


@pytest_asyncio.fixture(autouse=True)
async def setup_jwks_and_state():
    """Inject test JWKS and reset state replay cache for every test."""
    oidc_validator.set_jwks_cache_for_testing(TEST_JWKS)
    reset_consumed_states_for_testing()
    yield


@pytest_asyncio.fixture(autouse=True)
async def setup_test_db():
    """Initialize database tables for testing."""
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
    async with TestAsyncSessionLocal() as session:
        yield session


app.dependency_overrides[get_db] = override_get_db


@pytest_asyncio.fixture
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client


@pytest_asyncio.fixture
async def user_a_token() -> str:
    return create_test_jwt(sub="user-a-sub", email="user_a@example.com", name="User A")


@pytest_asyncio.fixture
async def user_b_token() -> str:
    return create_test_jwt(sub="user-b-sub", email="user_b@example.com", name="User B")
