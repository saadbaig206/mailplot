import uuid
from datetime import datetime
from typing import TYPE_CHECKING, Any, Optional

from sqlalchemy import JSON, DateTime, ForeignKey, Index, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import GUID, Base, utc_now

if TYPE_CHECKING:
    from src.models.user import User


class AuditEvent(Base):
    __tablename__ = "audit_events"

    id: Mapped[uuid.UUID] = mapped_column(
        GUID,
        primary_key=True,
        default=uuid.uuid4,
    )
    user_id: Mapped[uuid.UUID | None] = mapped_column(
        GUID,
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    event_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
        comment="Type of event (e.g. auth.login, oauth.connected, oauth.disconnected)",
    )
    ip_address: Mapped[str | None] = mapped_column(
        String(45),  # IPv6 support up to 45 chars
        nullable=True,
    )
    user_agent: Mapped[str | None] = mapped_column(
        String(512),
        nullable=True,
    )
    details: Mapped[dict[str, Any]] = mapped_column(
        JSON,
        default=dict,
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
        nullable=False,
        index=True,
    )

    # Relationships
    user: Mapped[Optional["User"]] = relationship(
        "User",
        back_populates="audit_events",
    )

    __table_args__ = (
        Index("ix_audit_events_user_event_time", "user_id", "event_type", "created_at"),
    )

    def __repr__(self) -> str:
        return f"<AuditEvent id={self.id} event_type={self.event_type} user_id={self.user_id}>"
