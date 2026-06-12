"""
dependencies.py

Purpose:
--------
Application-wide dependency management.

Responsibilities:
-----------------
- Create singleton RetrievalPipeline
- Create singleton RAGService
- Provide FastAPI dependency providers

Architecture Philosophy:
------------------------
Expensive components should be loaded once.

Application Startup
        ↓
RetrievalPipeline
        ↓
RAGService
        ↓
Request Handling
"""

from api.database.session import (
    SessionLocal,
)

from api.repositories.conversation_repository import (
    ConversationRepository,
)

from api.services.conversation_service import (
    ConversationService,
)

from api.services.rag_service import (
    RAGService,
)

from rag.pipelines.retrieval_pipeline import (
    RetrievalPipeline,
)


# ---------------------------------------------------------
# SINGLETONS
# ---------------------------------------------------------

retrieval_pipeline = (
    RetrievalPipeline()
)


# ---------------------------------------------------------
# DEPENDENCY PROVIDERS
# ---------------------------------------------------------

def get_rag_service() -> RAGService:

    db = SessionLocal()

    repository = (
        ConversationRepository(db)
    )

    conversation_service = (
        ConversationService(
            repository
        )
    )

    return RAGService(
        conversation_service=(
            conversation_service
        ),
        retrieval_pipeline=(
            retrieval_pipeline
        ),
    )