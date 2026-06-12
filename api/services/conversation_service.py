"""
conversation_service.py

Purpose:
--------
Conversation memory service for the
Hasanah Mart AI assistant.

Responsibilities:
-----------------
- Store conversation messages
- Retrieve conversation history
- Convert database models into
  service-layer models

Architecture Philosophy:
------------------------
Thin business layer.
Repository-backed memory.
Database-independent interface.
"""

from api.models.conversation import (
    ConversationHistory,
    ConversationMessage
)

from api.repositories.conversation_repository import (
    ConversationRepository
)


# ---------------------------------------------------------
# CONVERSATION SERVICE
# ---------------------------------------------------------

class ConversationService:

    """
    Conversation memory service.
    """

    # -----------------------------------------------------

    def __init__(
        self,
        repository: ConversationRepository
    ):

        self.repository = (
            repository
        )

    # -----------------------------------------------------
    # SAVE USER MESSAGE
    # -----------------------------------------------------

    def save_user_message(
        self,
        phone_number: str,
        content: str,
    ) -> None:

        self.repository.save_message(

            phone_number=phone_number,

            role="user",

            content=content
        )

    # -----------------------------------------------------
    # SAVE ASSISTANT MESSAGE
    # -----------------------------------------------------

    def save_assistant_message(
        self,
        phone_number: str,
        content: str,
    ) -> None:

        self.repository.save_message(

            phone_number=phone_number,

            role="assistant",

            content=content
        )

    # -----------------------------------------------------
    # GET RECENT HISTORY
    # -----------------------------------------------------

    def get_recent_history(
        self,
        phone_number: str,
        limit: int = 10,
    ) -> ConversationHistory:

        db_messages = (

            self.repository.get_history(

                phone_number=phone_number,

                limit=limit
            )
        )

        messages = [

            ConversationMessage(

                phone_number=(
                    msg.phone_number
                ),

                role=msg.role,

                content=msg.content,

                timestamp=(
                    msg.created_at
                )
            )

            for msg in db_messages
        ]

        return ConversationHistory(
            messages=messages
        )

    # -----------------------------------------------------
    # CLEAR HISTORY
    # -----------------------------------------------------

    def clear_history(
        self,
        phone_number: str,
    ) -> None:

        self.repository.clear_history(
            phone_number
        )