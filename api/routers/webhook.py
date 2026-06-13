"""
webhook.py

Purpose:
--------
WhatsApp webhook endpoints.

Responsibilities:
-----------------
- Handle Meta webhook verification
- Receive incoming WhatsApp events
- Log incoming payloads

Architecture Philosophy:
------------------------
Keep webhook layer thin.

WhatsApp
    ↓
Webhook
    ↓
Service Layer
"""

from fastapi import (
    APIRouter,
    HTTPException,
    Request,
)

from api.core.config import (
    settings
)

from api.core.logging import (
    get_logger
)

from api.services.rag_service import (
    RAGService
)

from api.services.whatsapp_service import (
    WhatsAppService
)

from fastapi import Depends

from api.dependencies.dependencies import (
    get_rag_service
)

from api.schemas.webhook import (
    WebhookPayload
)

from api.services.whatsapp_sender import (
    WhatsAppSender
)


# ---------------------------------------------------------
# LOGGING
# ---------------------------------------------------------

logger = get_logger(__name__)


# ---------------------------------------------------------
# ROUTER
# ---------------------------------------------------------

router = APIRouter(
    prefix="/webhook",
    tags=["WhatsApp"],
)

whatsapp_service = (
    WhatsAppService()
)

whatsapp_sender = (
    WhatsAppSender()
)


# ---------------------------------------------------------
# META VERIFICATION
# ---------------------------------------------------------

@router.get("")
async def verify_webhook(

    hub_mode: str | None = None,

    hub_verify_token: str | None = None,

    hub_challenge: str | None = None,
):

    """
    Meta webhook verification.

    GET /webhook
    """

    if (
        hub_mode == "subscribe"
        and hub_verify_token
        == settings.whatsapp_verify_token
    ):

        logger.info(
            "WhatsApp webhook verified."
        )

        return int(hub_challenge)

    raise HTTPException(
        status_code=403,
        detail="Verification failed.",
    )


# ---------------------------------------------------------
# RECEIVE EVENTS
# ---------------------------------------------------------

@router.post("")
async def receive_webhook(

    payload: WebhookPayload,

    rag_service: RAGService = Depends(
        get_rag_service
    ),
):

    whatsapp_payload = (
        payload.payload
    )

    logger.info(
        "Received WhatsApp webhook."
    )

    if not (
        whatsapp_service
        .is_message_event(
            whatsapp_payload
        )
    ):
        return {
            "status": "ignored"
        }

    phone_number, message_text = (
        whatsapp_service
        .extract_message(
            whatsapp_payload
        )
    )

    if not phone_number or not message_text:
        return {
            "status": "ignored"
        }

    logger.info(
        f"Phone: {phone_number}"
    )

    logger.info(
        f"Message: {message_text}"
    )

    answer = rag_service.ask(
        phone_number=phone_number,
        query=message_text,
    )

    response = (
        whatsapp_sender.send_text_message(
            phone_number=phone_number,
            message=answer,
        )
    )

    logger.info(
        f"Answer: {answer}"
    )

    logger.info(
        f"WhatsApp Response: {response}"
    )

    return {
        "status": "received"
    }