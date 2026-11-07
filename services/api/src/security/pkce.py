import base64
import hashlib
import re
import secrets


def generate_code_verifier(length: int = 64) -> str:
    """Generate a high-entropy cryptographic code_verifier for PKCE.

    Must be between 43 and 128 characters using unreserved characters [A-Z, a-z, 0-9, -, ., _, ~].
    """
    if length < 43 or length > 128:
        raise ValueError("PKCE code_verifier length must be between 43 and 128 characters")
    # Base64url without padding
    token = secrets.token_urlsafe(length)[:length]
    # Replace non-unreserved chars if any
    clean_token = re.sub(r"[^A-Za-z0-9\-\._~]", "A", token)
    return clean_token


def generate_code_challenge(verifier: str) -> str:
    """Generate the S256 code_challenge from a code_verifier.

    code_challenge = BASE64URL-ENCODE(SHA256(ASCII(code_verifier)))
    """
    if not verifier:
        raise ValueError("Verifier cannot be empty")
    digest = hashlib.sha256(verifier.encode("ascii")).digest()
    return base64.urlsafe_b64encode(digest).decode("ascii").rstrip("=")


def verify_code_challenge(verifier: str, expected_challenge: str) -> bool:
    """Validate that a verifier hashes to the expected S256 challenge."""
    if not verifier or not expected_challenge:
        return False
    actual_challenge = generate_code_challenge(verifier)
    return secrets.compare_digest(actual_challenge, expected_challenge)
