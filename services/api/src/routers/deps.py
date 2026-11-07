from typing import Annotated

from fastapi import Depends, HTTPException, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.models.user import User
from src.security.oidc_validator import OIDCValidationError, oidc_validator
from src.services.user_service import get_or_create_user_from_oidc_claims

security = HTTPBearer(auto_error=False)


async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Security(security)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> User:
    """Dependency that extracts and validates the Bearer token, resolving the User.

    Enforces that user identity is derived strictly from validated authentication.
    """
    if not credentials or not credentials.credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication token is missing",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = credentials.credentials
    try:
        claims = await oidc_validator.validate_token(token)
    except OIDCValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        ) from e

    user = await get_or_create_user_from_oidc_claims(db, claims)
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is deactivated",
        )

    await db.commit()
    await db.refresh(user, attribute_names=["email_accounts"])
    return user
