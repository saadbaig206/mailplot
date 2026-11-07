import uuid
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from src.models.audit_event import AuditEvent


async def log_audit_event(
    db: AsyncSession,
    event_type: str,
    user_id: uuid.UUID | None = None,
    ip_address: str | None = None,
    user_agent: str | None = None,
    details: dict[str, Any] | None = None,
) -> AuditEvent:
    """Record an immutable, sanitized audit entry for security monitoring."""
    event = AuditEvent(
        user_id=user_id,
        event_type=event_type,
        ip_address=ip_address,
        user_agent=user_agent,
        details=details or {},
    )
    db.add(event)
    await db.flush()
    return event
