import base64

from cryptography.fernet import Fernet, InvalidToken

from src.config import get_settings


class EncryptionError(Exception):
    """Raised when encryption or decryption fails or token is tampered."""

    pass


def _get_fernet() -> Fernet:
    settings = get_settings()
    key = settings.ENCRYPTION_KEY

    # Ensure key is 32 URL-safe base64-encoded bytes
    try:
        # If key is raw 32 bytes or already valid Fernet key
        if len(key) == 44 and key.endswith("="):
            return Fernet(key.encode("utf-8"))
        # Fallback derive 32-byte urlsafe base64
        derived = base64.urlsafe_b64encode(key.encode("utf-8").ljust(32)[:32])
        return Fernet(derived)
    except Exception as e:
        raise EncryptionError(f"Invalid encryption key configuration: {e}") from e


def encrypt_token(plaintext: str) -> str:
    """Encrypt a plaintext OAuth token into an authenticated ciphertext."""
    if not plaintext:
        raise EncryptionError("Cannot encrypt empty token")
    try:
        f = _get_fernet()
        ciphertext = f.encrypt(plaintext.encode("utf-8"))
        return ciphertext.decode("utf-8")
    except Exception as e:
        raise EncryptionError(f"Failed to encrypt token: {e}") from e


def decrypt_token(ciphertext: str) -> str:
    """Decrypt and verify the authenticated ciphertext back to plaintext.

    Raises EncryptionError if the ciphertext was modified, tampered, or invalid.
    """
    if not ciphertext:
        raise EncryptionError("Cannot decrypt empty ciphertext")
    try:
        f = _get_fernet()
        plaintext = f.decrypt(ciphertext.encode("utf-8"))
        return plaintext.decode("utf-8")
    except InvalidToken as e:
        raise EncryptionError("Decryption failed: Token is invalid, tampered, or corrupted") from e
    except Exception as e:
        raise EncryptionError(f"Decryption error: {e}") from e
