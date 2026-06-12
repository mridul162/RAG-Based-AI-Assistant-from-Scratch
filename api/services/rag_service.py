"""
rag_service.py

Purpose:
--------
Application-facing interface for the
Hasanah Mart RAG system.

Responsibilities:
-----------------
- Load conversation history
- Generate answers using RAG
- Provide a simple API layer

Architecture Philosophy:
------------------------
Thin orchestration layer.
Conversation-aware generation.
No transport-specific logic.
"""

from api.services.conversation_service import (
    ConversationService
)

from rag.generators.answer_generator import (
    AnswerGenerator
)
from rag.pipelines.retrieval_pipeline import RetrievalPipeline
from api.core.logging import get_logger

from api.services.query_rewrite_service import (
    QueryRewriteService
)

logging = get_logger(__name__)

# ---------------------------------------------------------
# RAG SERVICE
# ---------------------------------------------------------

class RAGService:

    """
    Conversation-aware RAG service.
    """

    # -----------------------------------------------------

    def __init__(
        self,
        conversation_service: ConversationService,
        retrieval_pipeline: RetrievalPipeline,
    ):

        self.conversation_service = (
            conversation_service
        )

        self.answer_generator = (
            AnswerGenerator(retrieval_pipeline)
        )

        self.query_rewrite_service = (
            QueryRewriteService()
        )

    # -----------------------------------------------------
    # ASK
    # -----------------------------------------------------

    def ask(
        self,
        phone_number: str,
        query: str,
    ) -> str:

        """
        Generate an answer using
        conversation history and RAG.
        """

        history = (

            self.conversation_service
            .get_recent_history(
                phone_number=phone_number,
                limit=10
            )
        )

        rewritten_query = (
            self.query_rewrite_service.rewrite(
                query=query,
                history=history,
            )
        )

        answer = (
            self.answer_generator.generate(

                query=rewritten_query,

                history=history,
            )
        )
        logging.info(
            f"Original Query: {query}"
        )

        logging.info(
            f"Rewritten Query: {rewritten_query}"
        )

        return answer