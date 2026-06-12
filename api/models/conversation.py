"""
conversation.py

Purpose:
--------
Conversation memory models for the
Hasanah Mart AI assistant.

Responsibilities:
-----------------
- Represent conversation messages
- Represent conversation history

Architecture Philosophy:
------------------------
Simple data structures.
Database-independent models.
Conversation-focused design.
"""

from dataclasses import (
    dataclass,
    field
)

from datetime import (
    datetime
)


# ---------------------------------------------------------
# CONVERSATION MESSAGE
# ---------------------------------------------------------

@dataclass
class ConversationMessage:

    phone_number: str
    role: str
    content: str
    timestamp: datetime


# ---------------------------------------------------------
# CONVERSATION HISTORY
# ---------------------------------------------------------

@dataclass
class ConversationHistory:

    messages: list[
        ConversationMessage
    ] = field(
        default_factory=list
    )