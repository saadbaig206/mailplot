import uuid

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.models.user import User
from src.routers.deps import get_current_user
from src.schemas.email_account import DisconnectResponse, EmailAccountResponse
from src.services.audit_service import log_audit_event
from src.services.email_account_service import (
    disconnect_account,
    list_user_email_accounts,
)

router = APIRouter(prefix="/email-accounts", tags=["Email Accounts"])


@router.get(
    "",
    response_model=list[EmailAccountResponse],
    status_code=status.HTTP_200_OK,
    summary="List Connected Email Accounts",
)
async def list_accounts(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """List all email accounts connected by the current user (strictly isolated)."""
    accounts = await list_user_email_accounts(db, user_id=current_user.id)
    return accounts


@router.delete(
    "/{account_id}",
    response_model=DisconnectResponse,
    status_code=status.HTTP_200_OK,
    summary="Disconnect & Revoke Email Account",
)
async def disconnect(
    account_id: uuid.UUID,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Disconnect and revoke OAuth tokens for an email account owned by the user.

    Strictly denies cross-user access (returns 404 if account does not belong to user).
    """
    success = await disconnect_account(db, user_id=current_user.id, account_id=account_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Email account not found or access denied",
        )

    await log_audit_event(
        db,
        event_type="oauth.disconnected",
        user_id=current_user.id,
        ip_address=request.client.host if request.client else None,
        user_agent=request.headers.get("user-agent"),
        details={"account_id": str(account_id)},
    )
    await db.commit()

    return DisconnectResponse(
        success=True,
        message="Email account successfully disconnected and revoked",
        email_account_id=account_id,
    )
