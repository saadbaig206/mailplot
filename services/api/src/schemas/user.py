import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict

from src.schemas.email_account import EmailAccountResponse


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    email: str
    full_name: str | None = None
    avatar_url: str | None = None
    is_active: bool
    created_at: datetime
    email_accounts: list[EmailAccountResponse] = []
