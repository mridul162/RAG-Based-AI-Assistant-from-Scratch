"""
conversation_repository.py

Purpose:
--------
Database access layer for conversation memory.

Responsibilities:
-----------------
- Save conversation messages
- Retrieve conversation history
- Clear conversation history

Architecture Philosophy:
------------------------
Repository pattern.
Database-only responsibilities.
No business logic.
"""

from sqlalchemy import (
    delete,
    select
)

from sqlalchemy.orm import (
    Session
)

from api.database.models.conversation import (
    ConversationMessageDB
)


# ---------------------------------------------------------
# REPOSITORY
# ---------------------------------------------------------

class ConversationRepository:

    """
    Repository for conversation messages.
    """

    # -----------------------------------------------------

    def __init__(
        self,
        db: Session
    ):

        self.db = db

    # -----------------------------------------------------
    # SAVE MESSAGE
    # -----------------------------------------------------

    def save_message(
        self,
        phone_number: str,
        role: str,
        content: str,
    ) -> ConversationMessageDB:

        """
        Save a conversation message.
        """

        message = ConversationMessageDB(

            phone_number=phone_number,

            role=role,

            content=content
        )

        self.db.add(
            message
        )

        self.db.commit()

        self.db.refresh(
            message
        )

        return message

    # -----------------------------------------------------
    # GET HISTORY
    # -----------------------------------------------------

    def get_history(
        self,
        phone_number: str,
        limit: int = 10,
    ) -> list[ConversationMessageDB]:

        """
        Retrieve recent conversation history.

        Returns oldest → newest order.
        """

        stmt = (

            select(
                ConversationMessageDB
            )

            .where(
                ConversationMessageDB.phone_number
                == phone_number
            )

            .order_by(
                ConversationMessageDB.created_at.desc()
            )

            .limit(limit)
        )

        messages = (

            self.db.execute(
                stmt
            )

            .scalars()
            .all()
        )

        return list(
            reversed(messages)
        )

    # -----------------------------------------------------
    # CLEAR HISTORY
    # -----------------------------------------------------

    def clear_history(
        self,
        phone_number: str,
    ) -> None:

        """
        Delete all messages for a user.
        """

        stmt = (

            delete(
                ConversationMessageDB
            )

            .where(
                ConversationMessageDB.phone_number
                == phone_number
            )
        )

        self.db.execute(
            stmt
        )

        self.db.commit()