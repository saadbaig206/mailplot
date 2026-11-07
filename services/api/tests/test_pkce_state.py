import uuid

import pytest

from src.security.pkce import (
    generate_code_challenge,
    generate_code_verifier,
    verify_code_challenge,
)
from src.security.state_signer import (
    OAuthStateError,
    create_oauth_state,
    verify_and_consume_state,
)


def test_pkce_generation_and_validation():
    """Verify PKCE code_verifier generation and S256 challenge verification."""
    verifier = generate_code_verifier(64)
    assert len(verifier) == 64
    # All characters must be unreserved URL characters
    assert all(
        c in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-._~" for c in verifier
    )

    challenge = generate_code_challenge(verifier)
    assert len(challenge) > 0
    # Must not contain '=' padding
    assert "=" not in challenge

    # Verification must succeed for matching pair
    assert verify_code_challenge(verifier, challenge) is True

    # Verification must fail for non-matching verifier
    other_verifier = generate_code_verifier(64)
    assert verify_code_challenge(other_verifier, challenge) is False


def test_state_creation_and_successful_consumption():
    """Verify state token lifecycle from creation to verification."""
    user_id = str(uuid.uuid4())
    provider = "google"
    verifier = generate_code_verifier()

    state = create_oauth_state(
        user_id=user_id, provider=provider, code_verifier=verifier, ttl_seconds=300
    )
    assert isinstance(state, str)
    assert len(state) > 30

    # Unpack and verify
    payload = verify_and_consume_state(
        state_token=state,
        expected_user_id=user_id,
        expected_provider=provider,
    )
    assert payload["user_id"] == user_id
    assert payload["provider"] == provider
    assert payload["code_verifier"] == verifier


def test_state_replay_protection():
    """Verify that reusing a consumed state raises OAuthStateError."""
    user_id = str(uuid.uuid4())
    provider = "microsoft"
    verifier = generate_code_verifier()

    state = create_oauth_state(
        user_id=user_id, provider=provider, code_verifier=verifier, ttl_seconds=300
    )

    # First consumption succeeds
    verify_and_consume_state(state, expected_user_id=user_id, expected_provider=provider)

    # Second consumption must raise replay error
    with pytest.raises(OAuthStateError, match="already been consumed"):
        verify_and_consume_state(state, expected_user_id=user_id, expected_provider=provider)


def test_state_user_mismatch_protection():
    """Verify that state generated for User A cannot be consumed by User B."""
    user_a = str(uuid.uuid4())
    user_b = str(uuid.uuid4())
    verifier = generate_code_verifier()

    state = create_oauth_state(user_id=user_a, provider="google", code_verifier=verifier)

    with pytest.raises(OAuthStateError, match="does not match the authenticated user"):
        verify_and_consume_state(state, expected_user_id=user_b, expected_provider="google")


def test_state_provider_mismatch_protection():
    """Verify that state generated for Google cannot be consumed for Microsoft."""
    user_id = str(uuid.uuid4())
    verifier = generate_code_verifier()

    state = create_oauth_state(user_id=user_id, provider="google", code_verifier=verifier)

    with pytest.raises(OAuthStateError, match="was issued for 'google', not 'microsoft'"):
        verify_and_consume_state(state, expected_user_id=user_id, expected_provider="microsoft")


def test_state_expiration():
    """Verify that expired state tokens are rejected."""
    user_id = str(uuid.uuid4())
    verifier = generate_code_verifier()

    # Create state with negative TTL (already expired)
    state = create_oauth_state(
        user_id=user_id, provider="google", code_verifier=verifier, ttl_seconds=-10
    )

    with pytest.raises(OAuthStateError, match="expired"):
        verify_and_consume_state(state, expected_user_id=user_id, expected_provider="google")


def test_state_tampering():
    """Verify that tampered ciphertext is rejected by authenticated decryption."""
    user_id = str(uuid.uuid4())
    verifier = generate_code_verifier()

    state = create_oauth_state(user_id=user_id, provider="google", code_verifier=verifier)
    tampered_state = state[:-5] + "XXXXX"

    with pytest.raises(OAuthStateError, match="Invalid or tampered"):
        verify_and_consume_state(
            tampered_state, expected_user_id=user_id, expected_provider="google"
        )
