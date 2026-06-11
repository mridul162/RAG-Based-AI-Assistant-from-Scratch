"""
retrieval_pipeline.py

Purpose:
--------
Retrieval pipeline for the
Hasanah Mart multilingual RAG system.

Pipeline:
---------
1. Load FAISS index
2. Initialize retriever
3. Execute semantic search
4. Return retrieved chunks

Architecture:
-------------
User Query
    ↓
Retrieval Pipeline
    ↓
Retriever
    ↓
FAISS Search
    ↓
Retrieved Chunks
"""

from api.core.config import (
    settings
)

from api.core.logging import (
    get_logger,
    setup_logging
)

from rag.embedders.openai_embedder import (
    OpenAIEmbedder
)

from rag.vectorstores.faiss_store import (
    FAISSStore
)

from rag.retrievers.retriever import (
    Retriever
)


# ---------------------------------------------------------
# LOGGING
# ---------------------------------------------------------

setup_logging()

logger = get_logger(__name__)


# ---------------------------------------------------------
# RETRIEVAL PIPELINE
# ---------------------------------------------------------

class RetrievalPipeline:

    """
    End-to-end retrieval pipeline.
    """

    def __init__(self):

        logger.info(
            "Initializing retrieval pipeline..."
        )

        # -------------------------------------------------
        # EMBEDDER
        # -------------------------------------------------

        self.embedder = (
            OpenAIEmbedder()
        )

        # -------------------------------------------------
        # VECTOR STORE
        # -------------------------------------------------

        self.vector_store = (
            FAISSStore(
                embedding_dimension=(
                    settings.embedding_dimension
                )
            )
        )

        self.vector_store.load(
            index_path=(
                settings.faiss_index_path
            ),
            metadata_path=(
                settings.faiss_metadata_path
            )
        )

        logger.info(
            f"Loaded "
            f"{self.vector_store.total_vectors()} "
            f"vectors."
        )

        # -------------------------------------------------
        # RETRIEVER
        # -------------------------------------------------

        self.retriever = (
            Retriever(
                embedder=self.embedder,
                vector_store=self.vector_store
            )
        )

        logger.info(
            "Retrieval pipeline initialized."
        )

    # -----------------------------------------------------

    def retrieve(
        self,
        query: str,
        top_k: int = 5
    ):

        logger.info(
            f"Processing query: {query}"
        )

        return self.retriever.retrieve(
            query=query,
            top_k=top_k
        )


# ---------------------------------------------------------
# TESTING
# ---------------------------------------------------------

if __name__ == "__main__":

    pipeline = RetrievalPipeline()

    query = (
        "What are the benefits of khalisha honey?"
    )

    results = pipeline.retrieve(
        query=query,
        top_k=5
    )

    print("\n" + "=" * 70)
    print("RETRIEVAL RESULTS")
    print("=" * 70)

    print(f"\nQuery: {query}")

    for i, result in enumerate(
        results,
        start=1
    ):

        print("\n" + "-" * 70)

        print(
            f"RESULT #{i}"
        )

        print("-" * 70)

        print(
            f"Score: "
            f"{result.score:.4f}"
        )

        print(
            f"Product ID: "
            f"{result.metadata.get('product_id')}"
        )

        print(
            f"Heading: "
            f"{result.metadata.get('heading')}"
        )

        print("\nText:")

        print(result.text)