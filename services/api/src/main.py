from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.config import get_settings
from src.database import engine
from src.models import Base
from src.routers import email_accounts, health, me, oauth

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # If running with SQLite, create tables if they don't exist yet
    if "sqlite" in settings.DATABASE_URL:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


app = FastAPI(
    title="MailPilot AI — Core API",
    description="Multi-user AI email management SaaS platform backend.",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(health.router)  # /health
app.include_router(health.router, prefix=settings.API_V1_STR)  # /api/v1/health
app.include_router(me.router, prefix=settings.API_V1_STR)  # /api/v1/me
app.include_router(email_accounts.router, prefix=settings.API_V1_STR)  # /api/v1/email-accounts
app.include_router(oauth.router, prefix=settings.API_V1_STR)  # /api/v1/oauth


@app.get("/", include_in_schema=False)
async def root():
    return {
        "service": "MailPilot AI API",
        "version": "1.0.0",
        "status": "operational",
        "docs": "/docs",
    }
