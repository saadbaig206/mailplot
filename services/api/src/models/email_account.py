import uuid
from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import JSON, DateTime, ForeignKey, Index, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import GUID, Base, TimestampMixin, utc_now

if TYPE_CHECKING:
    from src.models.oauth_connection import OAuthConnection
    from src.models.user import User


class EmailAccount(Base, TimestampMixin):
    __tablename__ = "email_accounts"

    id: Mapped[uuid.UUID] = mapped_column(
        GUID,
        primary_key=True,
        default=uuid.uuid4,
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        GUID,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    provider: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        comment="OAuth provider: google or microsoft",
    )
    email_address: Mapped[str] = mapped_column(
        String(320),
        nullable=False,
        index=True,
    )
    display_name: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )
    status: Mapped[str] = mapped_column(
        String(50),
        default="active",
        nullable=False,
        comment="Status: active, disconnected, expired, revoked",
    )
    scopes: Mapped[list[str]] = mapped_column(
        JSON,
        default=list,
        nullable=False,
    )
    connected_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
        nullable=False,
    )
    last_synced_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    # Relationships
    user: Mapped["User"] = relationship(
        "User",
        back_populates="email_accounts",
    )
    oauth_connection: Mapped[Optional["OAuthConnection"]] = relationship(
        "OAuthConnection",
        back_populates="email_account",
        uselist=False,
        cascade="all, delete-orphan",
    )

    __table_args__ = (
        Index("ix_email_accounts_user_provider", "user_id", "provider"),
        Index("ix_email_accounts_user_email", "user_id", "email_address", unique=True),
    )

    def __repr__(self) -> str:
        return f"<EmailAccount id={self.id} user_id={self.user_id} provider={self.provider} email={self.email_address}>"
