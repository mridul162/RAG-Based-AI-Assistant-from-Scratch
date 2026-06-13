from pydantic import BaseModel

class WebhookPayload(BaseModel):
    payload: dict