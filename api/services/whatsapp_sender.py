"""
whatsapp_sender.py

Purpose:
--------
Send outgoing WhatsApp messages using
the WhatsApp Cloud API.

Responsibilities:
-----------------
- Send text messages
- Handle WhatsApp API requests
- Isolate WhatsApp transport logic

Architecture Philosophy:
------------------------
Webhook
    ↓
RAG Service
    ↓
WhatsApp Sender
    ↓
WhatsApp Cloud API
"""

import requests

from api.core.config import settings
from api.core.logging import get_logger


logger = get_logger(__name__)


# ---------------------------------------------------------
# WHATSAPP SENDER
# ---------------------------------------------------------

class WhatsAppSender:

    """
    WhatsApp Cloud API sender.
    """

    def __init__(self):

        self.phone_number_id = (
            settings.whatsapp_phone_number_id
        )

        self.access_token = (
            settings.whatsapp_access_token
        )

        self.base_url = (
            f"https://graph.facebook.com/v23.0/"
            f"{self.phone_number_id}/messages"
        )

    # -----------------------------------------------------

    def send_text_message(
        self,
        phone_number: str,
        message: str,
    ) -> dict:

        """
        Send a WhatsApp text message.
        """

        headers = {

            "Authorization":
            f"Bearer {self.access_token}",

            "Content-Type":
            "application/json",
        }

        payload = {

            "messaging_product":
            "whatsapp",

            "recipient_type":
            "individual",

            "to":
            phone_number,

            "type":
            "text",

            "text": {

                "preview_url":
                False,

                "body":
                message,
            },
        }

        response = requests.post(

            self.base_url,

            headers=headers,

            json=payload,
            
        )

        logger.error(
            f"Status Code: {response.status_code}"
        )

        logger.error(
            f"Response Body: {response.text}"
        )

        response.raise_for_status()

        logger.info(
            f"WhatsApp message sent to "
            f"{phone_number}"
        )

        return response.json()