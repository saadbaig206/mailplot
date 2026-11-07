from fastapi import APIRouter, Depends, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.models.user import User
from src.routers.deps import get_current_user
from src.schemas.user import UserResponse
from src.services.audit_service import log_audit_event

router = APIRouter(prefix="/me", tags=["User Profile"])


@router.get(
    "",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Get Authenticated User Profile",
)
async def get_me(
    request: Request,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Returns the authenticated user's profile and connected email accounts.

    Enforces that user identity is derived strictly from validated authentication.
    """
    await log_audit_event(
        db,
        event_type="auth.me_accessed",
        user_id=current_user.id,
        ip_address=request.client.host if request.client else None,
        user_agent=request.headers.get("user-agent"),
    )
    await db.commit()
    return current_user
