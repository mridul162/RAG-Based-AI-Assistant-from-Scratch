from api.database.session import SessionLocal
from api.repositories.conversation_repository import ConversationRepository
from api.services.conversation_service import ConversationService
from api.services.rag_service import RAGService
from rag.pipelines.retrieval_pipeline import (
    RetrievalPipeline
)

db = SessionLocal()

repo = (
    ConversationRepository(db)
)

conversation_service = (
    ConversationService(repo)
)

retrieval_pipeline = (
    RetrievalPipeline()
)

rag_service = (
    RAGService(
        conversation_service,
        retrieval_pipeline
    )
)

# conversation_service.clear_history(
#     "8801712345678"
# )

# conversation_service.save_user_message(
#     "8801712345678",
#     "Tell me about Kholisha Honey."
# )

# conversation_service.save_assistant_message(
#     "8801712345678",
#     "Kholisha Honey is collected from Sundarbans forest."
# )

answer = rag_service.ask(

    phone_number="8801712345678",

    query="Where do collected it from?"
)

print(answer)