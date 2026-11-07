from datetime import datetime

from pydantic import BaseModel, ConfigDict


class HealthResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    status: str
    environment: str
    database: str
    timestamp: datetime
