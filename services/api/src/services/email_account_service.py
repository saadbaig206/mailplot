import uuid
from datetime import UTC, datetime, timedelta
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.models.email_account import EmailAccount
from src.models.oauth_connection import OAuthConnection
from src.oauth import get_oauth_provider
from src.security.encryption import decrypt_token, encrypt_token


class EmailAccountServiceError(Exception):
    pass


async def list_user_email_accounts(
    db: AsyncSession,
    user_id: uuid.UUID,
) -> list[EmailAccount]:
    """Retrieve all email accounts owned by the specified user (tenant isolation)."""
    stmt = (
        select(EmailAccount)
        .where(EmailAccount.user_id == user_id)
        .order_by(EmailAccount.created_at.desc())
    )
    result = await db.execute(stmt)
    return list(result.scalars().all())


async def get_user_email_account(
    db: AsyncSession,
    user_id: uuid.UUID,
    account_id: uuid.UUID,
) -> EmailAccount | None:
    """Retrieve an email account strictly enforcing user ownership."""
    stmt = (
        select(EmailAccount)
        .options(selectinload(EmailAccount.oauth_connection))
        .where(EmailAccount.id == account_id, EmailAccount.user_id == user_id)
    )
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def connect_or_update_account(
    db: AsyncSession,
    user_id: uuid.UUID,
    provider_name: str,
    tokens: dict[str, Any],
    profile: dict[str, Any],
) -> EmailAccount:
    """Store or update a connected mailbox with encrypted OAuth credentials."""
    email_address = profile.get("email")
    display_name = profile.get("display_name")
    if not email_address:
        raise EmailAccountServiceError("Cannot connect email account without a valid email address")

    # 1. Encrypt sensitive tokens with authenticated encryption
    raw_access_token = tokens["access_token"]
    raw_refresh_token = tokens.get("refresh_token")

    encrypted_access = encrypt_token(raw_access_token)
    encrypted_refresh = encrypt_token(raw_refresh_token) if raw_refresh_token else None

    # Calculate token expiration
    expires_in = tokens.get("expires_in", 3600)
    expires_at = datetime.now(UTC) + timedelta(seconds=expires_in)

    # 2. Check if this mailbox is already connected for this user
    stmt = (
        select(EmailAccount)
        .options(selectinload(EmailAccount.oauth_connection))
        .where(EmailAccount.user_id == user_id, EmailAccount.email_address == email_address)
    )
    result = await db.execute(stmt)
    account = result.scalar_one_or_none()

    if account:
        account.status = "active"
        account.provider = provider_name
        account.display_name = display_name
        account.scopes = tokens.get("scopes", [])
        account.last_synced_at = None

        conn = account.oauth_connection
        if conn:
            conn.encrypted_access_token = encrypted_access
            if encrypted_refresh:
                conn.encrypted_refresh_token = encrypted_refresh
            conn.token_type = tokens.get("token_type", "Bearer")
            conn.expires_at = expires_at
            conn.extra_metadata = tokens.get("raw_response", {})
        else:
            conn = OAuthConnection(
                email_account_id=account.id,
                provider=provider_name,
                encrypted_access_token=encrypted_access,
                encrypted_refresh_token=encrypted_refresh,
                token_type=tokens.get("token_type", "Bearer"),
                expires_at=expires_at,
                extra_metadata=tokens.get("raw_response", {}),
            )
            db.add(conn)
    else:
        account = EmailAccount(
            user_id=user_id,
            provider=provider_name,
            email_address=email_address,
            display_name=display_name,
            status="active",
            scopes=tokens.get("scopes", []),
        )
        db.add(account)
        await db.flush()

        conn = OAuthConnection(
            email_account_id=account.id,
            provider=provider_name,
            encrypted_access_token=encrypted_access,
            encrypted_refresh_token=encrypted_refresh,
            token_type=tokens.get("token_type", "Bearer"),
            expires_at=expires_at,
            extra_metadata=tokens.get("raw_response", {}),
        )
        db.add(conn)

    await db.flush()
    return account


async def disconnect_account(
    db: AsyncSession,
    user_id: uuid.UUID,
    account_id: uuid.UUID,
) -> bool:
    """Safely revoke tokens with the provider and delete or disconnect the account."""
    account = await get_user_email_account(db, user_id=user_id, account_id=account_id)
    if not account:
        return False

    # Attempt provider revocation if connection and tokens exist
    if account.oauth_connection:
        try:
            provider = get_oauth_provider(account.provider)
            # Try revoking refresh token first, then access token
            token_to_revoke = None
            if account.oauth_connection.encrypted_refresh_token:
                token_to_revoke = decrypt_token(account.oauth_connection.encrypted_refresh_token)
            elif account.oauth_connection.encrypted_access_token:
                token_to_revoke = decrypt_token(account.oauth_connection.encrypted_access_token)

            if token_to_revoke:
                await provider.revoke_token(token_to_revoke)
        except Exception:
            # Continue disconnect even if remote revoke network call fails
            pass

    # Delete the account (cascades to oauth_connections)
    await db.delete(account)
    await db.flush()
    return True
