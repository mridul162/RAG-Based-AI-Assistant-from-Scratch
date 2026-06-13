"""
whatsapp_service.py

Purpose:
--------
Process incoming WhatsApp webhook payloads.

Responsibilities:
-----------------
- Detect message events
- Extract sender phone number
- Extract message text
- Hide WhatsApp payload structure
  from the rest of the application

Architecture Philosophy:
------------------------
Webhook
    ↓
WhatsAppService
    ↓
Clean Python data

Keep payload parsing isolated.
"""

from typing import Optional


# ---------------------------------------------------------
# WHATSAPP SERVICE
# ---------------------------------------------------------

class WhatsAppService:

    """
    WhatsApp webhook payload parser.
    """

    # -----------------------------------------------------

    def is_message_event(
        self,
        payload: dict,
    ) -> bool:

        """
        Check whether the webhook
        contains a user message.
        """

        try:

            messages = (
                payload["entry"][0]
                ["changes"][0]
                ["value"]["messages"]
            )

            return len(messages) > 0

        except (
            KeyError,
            IndexError,
            TypeError,
        ):

            return False

    # -----------------------------------------------------

    def extract_phone_number(
        self,
        payload: dict,
    ) -> Optional[str]:

        """
        Extract sender phone number.
        """

        try:

            return (
                payload["entry"][0]
                ["changes"][0]
                ["value"]["messages"][0]
                ["from"]
            )

        except (
            KeyError,
            IndexError,
            TypeError,
        ):

            return None

    # -----------------------------------------------------

    def extract_message_text(
        self,
        payload: dict,
    ) -> Optional[str]:

        """
        Extract user message text.
        """

        try:

            return (
                payload["entry"][0]
                ["changes"][0]
                ["value"]["messages"][0]
                ["text"]["body"]
            )

        except (
            KeyError,
            IndexError,
            TypeError,
        ):

            return None

    # -----------------------------------------------------

    def extract_message(
        self,
        payload: dict,
    ) -> tuple[Optional[str], Optional[str]]:

        """
        Extract both phone number
        and message text.
        """

        phone_number = (
            self.extract_phone_number(
                payload
            )
        )

        message_text = (
            self.extract_message_text(
                payload
            )
        )

        return (
            phone_number,
            message_text,
        )


# ---------------------------------------------------------
# TEST
# ---------------------------------------------------------

if __name__ == "__main__":

    payload = {

        "object":
        "whatsapp_business_account",

        "entry": [

            {

                "changes": [

                    {

                        "value": {

                            "messages": [

                                {

                                    "from":
                                    "8801712345678",

                                    "text": {

                                        "body":
                                        (
                                            "Tell me about "
                                            "Kholisha Honey"
                                        )
                                    }
                                }
                            ]
                        }
                    }
                ]
            }
        ]
    }

    service = WhatsAppService()

    print(
        service.is_message_event(
            payload
        )
    )

    print(
        service.extract_phone_number(
            payload
        )
    )

    print(
        service.extract_message_text(
            payload
        )
    )

    print(
        service.extract_message(
            payload
        )
    )

if __name__ == "__main__":
    payload = {
        "object": "whatsapp_business_account",
        "entry": [
            {
                "changes": [
                    {
                        "value": {
                            "messages": [
                                {
                                    "from": "8801712345678",
                                    "text": {
                                        "body": "Tell me about Kalojira Honey"
                                    }
                                }
                            ]
                        }
                    }
                ]
            }
        ]
    }

    service = WhatsAppService()

    print(
        service.extract_message(
            payload
        )
    )