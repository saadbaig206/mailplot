from datetime import UTC, datetime

from fastapi import APIRouter, Depends, status
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import get_settings
from src.database import get_db
from src.schemas.common import HealthResponse

router = APIRouter(tags=["Health"])


@router.get(
    "/health",
    response_model=HealthResponse,
    status_code=status.HTTP_200_OK,
    summary="Service Health Check",
)
async def check_health(db: AsyncSession = Depends(get_db)):
    """Health check endpoint probing application status and database connectivity."""
    settings = get_settings()
    db_status = "healthy"
    try:
        await db.execute(text("SELECT 1"))
    except Exception as e:
        db_status = f"unhealthy: {e}"

    return HealthResponse(
        status="ok" if db_status == "healthy" else "degraded",
        environment=settings.ENVIRONMENT,
        database=db_status,
        timestamp=datetime.now(UTC),
    )
