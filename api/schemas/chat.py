"""
chat.py

Purpose:
--------
Request and response schemas for the chat API.

Responsibilities:
-----------------
- Validate incoming chat requests
- Define API response contracts
- Provide typed request/response models

Architecture Philosophy:
------------------------
Keep schemas simple.
Represent only API contracts.
No business logic.
"""

from pydantic import BaseModel


# ---------------------------------------------------------
# REQUEST
# ---------------------------------------------------------

class ChatRequest(BaseModel):

    """
    Incoming chat request.
    """

    phone_number: str

    message: str


# ---------------------------------------------------------
# RESPONSE
# ---------------------------------------------------------

class ChatResponse(BaseModel):

    """
    Chat API response.
    """

    answer: str