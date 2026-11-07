from pydantic import BaseModel, ConfigDict

from src.schemas.email_account import EmailAccountResponse


class OAuthStartResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    provider: str
    authorization_url: str


class OAuthCallbackRequest(BaseModel):
    code: str
    state: str


class OAuthCallbackResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    success: bool
    account: EmailAccountResponse
    message: str
