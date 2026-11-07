import uuid
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.models.user import User


async def get_user_by_id(db: AsyncSession, user_id: uuid.UUID) -> User | None:
    stmt = select(User).options(selectinload(User.email_accounts)).where(User.id == user_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def get_or_create_user_from_oidc_claims(
    db: AsyncSession,
    claims: dict[str, Any],
) -> User:
    """Resolve an application user from validated OIDC claims.

    Upserts user record based on external subject (`sub`) or verified email.
    """
    sub = claims.get("sub")
    email = claims.get("email") or f"{sub}@auth.mailpilot.local"
    full_name = claims.get("name") or claims.get("nickname")
    avatar_url = claims.get("picture")

    stmt = (
        select(User)
        .options(selectinload(User.email_accounts))
        .where((User.external_sub == sub) | (User.email == email))
    )
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()

    if user:
        # Update user attributes if changed
        if user.external_sub != sub:
            user.external_sub = sub
        if full_name and user.full_name != full_name:
            user.full_name = full_name
        if avatar_url and user.avatar_url != avatar_url:
            user.avatar_url = avatar_url
    else:
        user = User(
            external_sub=sub,
            email=email,
            full_name=full_name,
            avatar_url=avatar_url,
        )
        db.add(user)

    await db.flush()
    return user
