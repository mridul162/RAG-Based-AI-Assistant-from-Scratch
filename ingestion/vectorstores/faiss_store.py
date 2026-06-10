"""
faiss_store.py

Purpose:
--------
Store and retrieve multilingual semantic embeddings
using FAISS vector similarity search.

Responsibilities:
-----------------
- Create FAISS index
- Add embeddings to index
- Persist vector index
- Persist metadata mapping
- Load saved index
- Run semantic similarity search

This vector store DOES NOT:
---------------------------
- generate embeddings
- rerank retrieval
- perform hybrid search
- filter metadata
- orchestrate ingestion pipeline

Architecture Philosophy:
------------------------
Simple retrieval-first design.
Observability first.
Optimization later.
"""

import json
import sys

sys.stdout.reconfigure(encoding="utf-8")

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Any, List

import faiss
import numpy as np

from ingestion.models.embedding_models import EmbeddedChunk

from api.core.logging import (
    get_logger
    )

logger = get_logger(__name__)

# ---------------------------------------------------------
# SEARCH RESULT MODEL
# ---------------------------------------------------------

@dataclass
class RetrievalResult:
    """
    Semantic retrieval result.
    """

    score: float
    chunk_id: str
    text: str
    metadata: Dict[str, Any]


# ---------------------------------------------------------
# FAISS VECTOR STORE
# ---------------------------------------------------------

class FAISSStore:
    """
    Simple multilingual semantic vector store.
    """

    # -----------------------------------------------------

    def __init__(
        self,
        embedding_dimension: int,
    ):

        self.embedding_dimension = (
            embedding_dimension
        )

        # ---------------------------------------------
        # Inner Product Index
        # ---------------------------------------------

        self.index = faiss.IndexFlatIP(
            embedding_dimension
        )

        # ---------------------------------------------
        # Metadata Mapping
        # ---------------------------------------------

        self.metadata_store = []

    # -----------------------------------------------------

    def add_embeddings(
        self,
        embedded_chunks: List[EmbeddedChunk],
    ):
        """
        Add embedded chunks to FAISS index.
        """

        if not embedded_chunks:

            return

        vectors = []

        for chunk in embedded_chunks:

            vectors.append(
                chunk.embedding
            )

            self.metadata_store.append({

                "chunk_id": (
                    chunk.chunk_id
                ),

                "text": (
                    chunk.text
                ),

                "metadata": (
                    chunk.metadata
                ),
            })

        vectors = np.array(
            vectors,
            dtype=np.float32
        )

        self.index.add(vectors)

        logger.info(
            f"Added {len(vectors)} "
            f"embeddings to FAISS index."
        )

    # -----------------------------------------------------

    def search(
        self,
        query_embedding: List[float],
        top_k: int = 5,
    ) -> List[RetrievalResult]:
        """
        Perform semantic similarity search.
        """

        query_vector = np.array(
            [query_embedding],
            dtype=np.float32
        )

        scores, indices = self.index.search(
            query_vector,
            top_k
        )

        results = []

        for score, index_position in zip(
            scores[0],
            indices[0]
        ):

            # -----------------------------------------
            # Invalid index protection
            # -----------------------------------------

            if index_position < 0:
                continue

            metadata_item = (
                self.metadata_store[
                    index_position
                ]
            )

            result = RetrievalResult(

                score=float(score),

                chunk_id=(
                    metadata_item["chunk_id"]
                ),

                text=(
                    metadata_item["text"]
                ),

                metadata=(
                    metadata_item["metadata"]
                ),
            )

            results.append(result)

        return results

    # -----------------------------------------------------

    def save(
        self,
        index_path: str,
        metadata_path: str,
    ):
        """
        Persist FAISS index and metadata.
        """

        index_path = Path(index_path)

        metadata_path = Path(metadata_path)

        # ---------------------------------------------
        # Create directories
        # ---------------------------------------------

        index_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        metadata_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        # ---------------------------------------------
        # Save FAISS index
        # ---------------------------------------------

        faiss.write_index(
            self.index,
            str(index_path)
        )

        # ---------------------------------------------
        # Save metadata
        # ---------------------------------------------

        with open(
            metadata_path,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(

                self.metadata_store,

                f,

                ensure_ascii=False,

                indent=2,
            )

        logger.info("FAISS index saved.")

        logger.info(index_path)

        logger.info(metadata_path)

    # -----------------------------------------------------

    def load(
        self,
        index_path: str,
        metadata_path: str,
    ):
        """
        Load persisted FAISS index and metadata.
        """

        self.index = faiss.read_index(
            index_path
        )

        with open(
            metadata_path,
            "r",
            encoding="utf-8"
        ) as f:

            self.metadata_store = json.load(f)

        logger.info("FAISS index loaded.")

    # -----------------------------------------------------

    def total_vectors(
        self
    ) -> int:
        """
        Return total indexed vectors.
        """

        return self.index.ntotal


# ---------------------------------------------------------
# SIMPLE TEST EXECUTION
# ---------------------------------------------------------

if __name__ == "__main__":

    from ingestion.embedders.openai_embedder import (
        OpenAIEmbedder
    )

    # -----------------------------------------------------
    # Mock Embedded Chunk
    # -----------------------------------------------------

    # -----------------------------------------------------
    # Sample Texts
    # -----------------------------------------------------

    sample_texts = [

        "Pure Sundarbans honey rich in antioxidants.",

        "খাঁটি কাঁচা মধু প্রাকৃতিক পুষ্টিগুণে সমৃদ্ধ।",

        "Store honey in a cool dry place.",

        "500g honey price is ৳600.",
    ]

    # -----------------------------------------------------
    # Generate Embeddings
    # -----------------------------------------------------

    embedder = OpenAIEmbedder()

    embedded_chunks = []

    for i, text in enumerate(sample_texts):

        embedding = (
            embedder.embed_text(
                text
            )
        )

        embedded_chunks.append(

            EmbeddedChunk(

                chunk_id=f"chunk_{i}",

                text=text,

                embedding=embedding,

                metadata={
                    "source": "test"
                },
            )
        )

    # -----------------------------------------------------
    # Build FAISS Store
    # -----------------------------------------------------

    embedding_dimension = len(
        embedded_chunks[0].embedding
    )

    store = FAISSStore(
        embedding_dimension
    )

    store.add_embeddings(
        embedded_chunks
    )

    print(
        f"\nIndexed vectors: "
        f"{store.total_vectors()}"
    )

    # -----------------------------------------------------
    # Query Search
    # -----------------------------------------------------

    query = "raw honey benefits"

    query_embedding = (
        embedder.embed_text(
            query
        )
    )

    results = store.search(

        query_embedding=query_embedding,

        top_k=3,
    )

    # -----------------------------------------------------
    # Display Results
    # -----------------------------------------------------

    print("\n" + "=" * 70)
    print("RETRIEVAL RESULTS")
    print("=" * 70)

    print(f"\nQuery: {query}")

    for i, result in enumerate(
        results,
        start=1
    ):

        print("\n" + "-" * 70)

        print(f"RESULT #{i}")

        print("-" * 70)

        print(
            f"Score: {result.score:.4f}"
        )

        print(
            f"Chunk ID: {result.chunk_id}"
        )

        print("\nMetadata:")

        print(result.metadata)

        print("\nText:")

        print(result.text)

    # -----------------------------------------------------
    # Save Index
    # -----------------------------------------------------

    store.save(

        index_path=(
            "artifacts/embeddings/"
            "sample_index.faiss"
        ),

        metadata_path=(
            "artifacts/embeddings/"
            "sample_metadata.json"
        )
    )