import urllib.parse

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import get_settings
from src.database import get_db
from src.models.user import User
from src.oauth import get_oauth_provider
from src.oauth.base import OAuthProviderError
from src.routers.deps import get_current_user
from src.schemas.oauth import (
    OAuthCallbackRequest,
    OAuthCallbackResponse,
    OAuthStartResponse,
)
from src.security.pkce import generate_code_challenge, generate_code_verifier
from src.security.state_signer import (
    OAuthStateError,
    create_oauth_state,
    verify_and_consume_state,
)
from src.services.audit_service import log_audit_event
from src.services.email_account_service import connect_or_update_account

router = APIRouter(prefix="/oauth", tags=["OAuth Connections"])


@router.get(
    "/{provider}/start",
    response_model=OAuthStartResponse,
    status_code=status.HTTP_200_OK,
    summary="Initiate Mailbox OAuth Connection",
)
async def start_oauth(
    provider: str,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Initiates an OAuth connection flow for a supported provider (Google or Microsoft).

    Generates a cryptographically random PKCE code verifier, S256 code challenge,
    and a confidential, tamper-proof signed state token.
    """
    try:
        oauth_adapter = get_oauth_provider(provider)
    except OAuthProviderError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e

    # 1. Generate PKCE code verifier and S256 challenge
    code_verifier = generate_code_verifier(64)
    code_challenge = generate_code_challenge(code_verifier)

    # 2. Generate signed & encrypted state binding user_id, provider, and code_verifier
    state_token = create_oauth_state(
        user_id=str(current_user.id),
        provider=oauth_adapter.name,
        code_verifier=code_verifier,
        ttl_seconds=600,  # 10 minutes TTL
    )

    # 3. Build authorization URL
    auth_url = oauth_adapter.get_authorization_url(
        state=state_token,
        code_challenge=code_challenge,
    )

    await log_audit_event(
        db,
        event_type="oauth.start",
        user_id=current_user.id,
        ip_address=request.client.host if request.client else None,
        user_agent=request.headers.get("user-agent"),
        details={"provider": oauth_adapter.name},
    )
    await db.commit()

    return OAuthStartResponse(
        provider=oauth_adapter.name,
        authorization_url=auth_url,
    )


@router.post(
    "/{provider}/callback",
    response_model=OAuthCallbackResponse,
    status_code=status.HTTP_200_OK,
    summary="Complete Mailbox OAuth Connection (API)",
)
async def complete_oauth_callback(
    provider: str,
    body: OAuthCallbackRequest,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Process an OAuth authorization code, validating state, PKCE, and storing encrypted tokens."""
    try:
        oauth_adapter = get_oauth_provider(provider)
    except OAuthProviderError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e

    # 1. Verify and consume state (replay and tamper protection)
    try:
        state_data = verify_and_consume_state(
            state_token=body.state,
            expected_user_id=str(current_user.id),
            expected_provider=oauth_adapter.name,
        )
    except OAuthStateError as e:
        await log_audit_event(
            db,
            event_type="oauth.state_verification_failed",
            user_id=current_user.id,
            details={"provider": oauth_adapter.name, "reason": str(e)},
        )
        await db.commit()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e

    code_verifier = state_data["code_verifier"]

    # 2. Exchange code + verifier for tokens
    try:
        tokens = await oauth_adapter.exchange_code(code=body.code, code_verifier=code_verifier)
    except OAuthProviderError as e:
        await log_audit_event(
            db,
            event_type="oauth.token_exchange_failed",
            user_id=current_user.id,
            details={"provider": oauth_adapter.name, "error": str(e)},
        )
        await db.commit()
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"OAuth token exchange failed with provider: {e}",
        ) from e

    # 3. Fetch provider profile (email address)
    try:
        profile = await oauth_adapter.get_user_profile(access_token=tokens["access_token"])
    except OAuthProviderError as e:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Failed to fetch profile from provider: {e}",
        ) from e

    # 4. Save connected account with encrypted tokens
    account = await connect_or_update_account(
        db,
        user_id=current_user.id,
        provider_name=oauth_adapter.name,
        tokens=tokens,
        profile=profile,
    )

    await log_audit_event(
        db,
        event_type="oauth.connected",
        user_id=current_user.id,
        ip_address=request.client.host if request.client else None,
        user_agent=request.headers.get("user-agent"),
        details={
            "account_id": str(account.id),
            "provider": oauth_adapter.name,
            "email_address": account.email_address,
        },
    )
    await db.commit()

    return OAuthCallbackResponse(
        success=True,
        account=account,
        message=f"Successfully connected {oauth_adapter.name.title()} account {account.email_address}",
    )


@router.get(
    "/{provider}/callback",
    summary="Browser Redirect Handler for OAuth Consent",
    include_in_schema=False,
)
async def browser_oauth_callback(
    provider: str,
    code: str = Query(...),
    state: str = Query(...),
):
    """Redirects the browser back to the Next.js frontend with the authorization code and state."""
    settings = get_settings()
    frontend_base = (
        settings.ALLOWED_ORIGINS[0] if settings.ALLOWED_ORIGINS else "http://localhost:3000"
    )
    target = f"{frontend_base}/oauth/callback?provider={provider}&code={urllib.parse.quote(code)}&state={urllib.parse.quote(state)}"
    return RedirectResponse(url=target, status_code=status.HTTP_307_TEMPORARY_REDIRECT)
