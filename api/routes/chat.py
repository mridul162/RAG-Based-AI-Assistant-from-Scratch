"""
chat.py

Purpose:
--------
Chat API endpoints for the
Hasanah Mart RAG system.

Responsibilities:
-----------------
- Accept user chat requests
- Invoke RAG service
- Return generated answers
- Remain transport-layer only
"""

from fastapi import (
    APIRouter,
    Depends,
)

from api.schemas.chat import (
    ChatRequest,
    ChatResponse,
)

from api.services.rag_service import (
    RAGService,
)

from api.dependencies.dependencies import (
    get_rag_service
)

# ---------------------------------------------------------
# ROUTER
# ---------------------------------------------------------

router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)

# ---------------------------------------------------------
# CHAT ENDPOINT
# ---------------------------------------------------------

@router.post(
    "",
    response_model=ChatResponse,
)
def chat(
    request: ChatRequest,
    rag_service: RAGService = Depends(
        get_rag_service
    ),
) -> ChatResponse:

    answer = (
        rag_service.ask(
            phone_number=(
                request.phone_number
            ),
            query=request.message,
        )
    )

    return ChatResponse(
        answer=answer
    )