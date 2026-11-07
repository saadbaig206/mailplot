import json
import time
import uuid
from typing import Any

from src.security.encryption import decrypt_token, encrypt_token


class OAuthStateError(Exception):
    """Raised when an OAuth state token is invalid, expired, tampered, or replayed."""

    pass


# In-memory store for consumed state IDs to enforce single-use / replay protection
_CONSUMED_STATE_IDS: set[str] = set()


def create_oauth_state(
    user_id: str,
    provider: str,
    code_verifier: str,
    ttl_seconds: int = 600,
) -> str:
    """Create a confidential, authenticated, time-bounded OAuth state token."""
    payload = {
        "id": str(uuid.uuid4()),
        "user_id": str(user_id),
        "provider": provider,
        "code_verifier": code_verifier,
        "exp": int(time.time()) + ttl_seconds,
    }
    raw_json = json.dumps(payload)
    return encrypt_token(raw_json)


def verify_and_consume_state(
    state_token: str,
    expected_user_id: str,
    expected_provider: str,
) -> dict[str, Any]:
    """Verify, unpack, and consume an OAuth state token.

    Validates:
    - Authenticity and decryption integrity
    - Expiration (TTL)
    - Matching expected user ID (tenant protection)
    - Matching expected provider
    - Single-use replay protection
    """
    if not state_token:
        raise OAuthStateError("Missing OAuth state parameter")

    try:
        raw_json = decrypt_token(state_token)
        payload = json.loads(raw_json)
    except Exception as e:
        raise OAuthStateError("Invalid or tampered OAuth state parameter") from e

    state_id = payload.get("id")
    if not state_id:
        raise OAuthStateError("Malformed OAuth state parameter")

    if state_id in _CONSUMED_STATE_IDS:
        raise OAuthStateError("OAuth state has already been consumed (replay detected)")

    exp = payload.get("exp", 0)
    if time.time() > exp:
        raise OAuthStateError("OAuth state has expired")

    user_id = payload.get("user_id")
    if str(user_id) != str(expected_user_id):
        raise OAuthStateError("OAuth state does not match the authenticated user")

    provider = payload.get("provider")
    if provider != expected_provider:
        raise OAuthStateError(f"OAuth state was issued for '{provider}', not '{expected_provider}'")

    code_verifier = payload.get("code_verifier")
    if not code_verifier:
        raise OAuthStateError("OAuth state missing code verifier")

    # Mark as consumed
    _CONSUMED_STATE_IDS.add(state_id)

    return payload


def reset_consumed_states_for_testing() -> None:
    """Helper for unit tests."""
    global _CONSUMED_STATE_IDS
    _CONSUMED_STATE_IDS.clear()
