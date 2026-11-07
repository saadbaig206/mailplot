import pytest

from src.security.encryption import (
    EncryptionError,
    decrypt_token,
    encrypt_token,
)


def test_encryption_decryption_roundtrip():
    """Verify that sensitive OAuth tokens can be encrypted and accurately decrypted."""
    raw_token = "ya29.a0AfH6SMD_MockOAuthAccessToken_Secret123456789"
    ciphertext = encrypt_token(raw_token)

    assert isinstance(ciphertext, str)
    assert ciphertext != raw_token
    assert raw_token not in ciphertext

    decrypted = decrypt_token(ciphertext)
    assert decrypted == raw_token


def test_encryption_tamper_detection():
    """Verify that any modification to ciphertext causes authenticated decryption to fail."""
    raw_token = "refresh_token_very_secret_value_98765"
    ciphertext = encrypt_token(raw_token)

    # Tamper with the ciphertext (e.g., bit flip or modify character)
    tampered = ciphertext[:-4] + ("A" if ciphertext[-4] != "A" else "B") + ciphertext[-3:]

    with pytest.raises(EncryptionError, match="Decryption failed"):
        decrypt_token(tampered)


def test_empty_token_rejection():
    """Verify that attempting to encrypt or decrypt empty input raises EncryptionError."""
    with pytest.raises(EncryptionError):
        encrypt_token("")

    with pytest.raises(EncryptionError):
        decrypt_token("")
