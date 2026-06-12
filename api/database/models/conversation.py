"""
conversation.py

Purpose:
--------
Database model for conversation memory.

Responsibilities:
-----------------
- Persist conversation messages
- Support conversation history retrieval

Architecture Philosophy:
------------------------
Simple schema.
WhatsApp-oriented design.
Memory-first approach.
"""

from datetime import (
    datetime,
    UTC
)

from sqlalchemy import (
    DateTime,
    Integer,
    String,
    Text
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column
)

from api.database.base import (
    Base
)


# ---------------------------------------------------------
# CONVERSATION MESSAGE
# ---------------------------------------------------------

class ConversationMessageDB(Base):

    """
    Persistent conversation message.
    """

    __tablename__ = (
        "conversation_messages"
    )

    # -----------------------------------------------------
    # PRIMARY KEY
    # -----------------------------------------------------

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    # -----------------------------------------------------
    # USER IDENTIFIER
    # -----------------------------------------------------

    phone_number: Mapped[str] = (
        mapped_column(
            String(30),
            nullable=False,
            index=True
        )
    )

    # -----------------------------------------------------
    # MESSAGE ROLE
    # -----------------------------------------------------

    role: Mapped[str] = (
        mapped_column(
            String(20),
            nullable=False
        )
    )

    # -----------------------------------------------------
    # MESSAGE CONTENT
    # -----------------------------------------------------

    content: Mapped[str] = (
        mapped_column(
            Text,
            nullable=False
        )
    )

    # -----------------------------------------------------
    # TIMESTAMP
    # -----------------------------------------------------

    created_at: Mapped[datetime] = (
        mapped_column(
            DateTime(timezone=True),
            nullable=False,
            default=lambda: (
                datetime.now(UTC)
            )
        )
    )