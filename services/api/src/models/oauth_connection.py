import uuid
from datetime import datetime
from typing import TYPE_CHECKING, Any

from sqlalchemy import JSON, DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import GUID, Base, TimestampMixin

if TYPE_CHECKING:
    from src.models.email_account import EmailAccount


class OAuthConnection(Base, TimestampMixin):
    __tablename__ = "oauth_connections"

    id: Mapped[uuid.UUID] = mapped_column(
        GUID,
        primary_key=True,
        default=uuid.uuid4,
    )
    email_account_id: Mapped[uuid.UUID] = mapped_column(
        GUID,
        ForeignKey("email_accounts.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
        index=True,
    )
    provider: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        comment="OAuth provider: google or microsoft",
    )
    encrypted_access_token: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        comment="Authenticated ciphertext of provider access token",
    )
    encrypted_refresh_token: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        comment="Authenticated ciphertext of provider refresh token",
    )
    token_type: Mapped[str] = mapped_column(
        String(50),
        default="Bearer",
        nullable=False,
    )
    expires_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    extra_metadata: Mapped[dict[str, Any]] = mapped_column(
        JSON,
        default=dict,
        nullable=False,
        comment="Non-sensitive provider metadata (e.g. granted scope string, token id)",
    )

    # Relationships
    email_account: Mapped["EmailAccount"] = relationship(
        "EmailAccount",
        back_populates="oauth_connection",
    )

    def __repr__(self) -> str:
        return f"<OAuthConnection id={self.id} provider={self.provider} email_account_id={self.email_account_id}>"
