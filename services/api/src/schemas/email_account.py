import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class EmailAccountResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    provider: str
    email_address: str
    display_name: str | None = None
    status: str
    scopes: list[str]
    connected_at: datetime
    last_synced_at: datetime | None = None


class DisconnectResponse(BaseModel):
    success: bool
    message: str
    email_account_id: uuid.UUID
