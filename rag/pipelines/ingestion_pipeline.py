"""
ingestion_pipeline.py

Purpose:
--------
Main orchestration pipeline for the Hasanah Mart
multilingual RAG ingestion system.

Current Pipeline Stages:
------------------------
1. Validate KB
2. Load markdown documents
3. Parse semantic sections
4. Normalize content
5. Generate semantic chunks
6. Persist artifacts
7. Generate ingestion summary

Architecture Philosophy:
------------------------
- retrieval-first
- observable
- modular
- semantically stable
- multilingual-safe
"""

import sys
sys.stdout.reconfigure(encoding="utf-8")

from pathlib import Path
from collections import Counter

# ---------------------------------------------------------
# LOADERS
# ---------------------------------------------------------

from rag.loaders.markdown_loader import (
    MarkdownLoader
)

from rag.loaders.product_metadata_loader import (
    ProductMetadataLoader
)

# ---------------------------------------------------------
# VALIDATORS
# ---------------------------------------------------------

from rag.validators.kb_validator import (
    KBValidator,
    print_validation_report
)

# ---------------------------------------------------------
# PARSERS
# ---------------------------------------------------------

from rag.parsers.markdown_parser import (
    MarkdownParser
)

# ---------------------------------------------------------
# NORMALIZERS
# ---------------------------------------------------------

from rag.utils.normalizer import (
    TextNormalizer
)

# ---------------------------------------------------------
# CHUNKERS
# ---------------------------------------------------------

from rag.chunkers.semantic_chunker import (
    SemanticChunker
)

# ---------------------------------------------------------
# ARTIFACTS
# ---------------------------------------------------------

from rag.utils.artifact_writer import (
    ArtifactWriter
)


# ---------------------------------------------------------
# INGESTION PIPELINE
# ---------------------------------------------------------

class IngestionPipeline:
    """
    Main ingestion orchestrator.
    """

    def __init__(
        self,
        kb_root: str,
    ):

        self.kb_root = Path(kb_root)

        # -------------------------------------------------
        # Initialize Components
        # -------------------------------------------------

        self.validator = KBValidator(
            kb_root=str(self.kb_root)
        )

        self.loader = MarkdownLoader(
            kb_root=str(self.kb_root)
        )

        self.metadata_loader = ProductMetadataLoader(
            kb_root=str(self.kb_root)
        )

        self.parser = MarkdownParser()

        self.normalizer = TextNormalizer()

        self.chunker = SemanticChunker()

        self.artifact_writer = ArtifactWriter()

    # -----------------------------------------------------

    def run(self):
        """
        Execute full ingestion pipeline.
        """

        self._print_pipeline_header()

        # -------------------------------------------------
        # STEP 1 — VALIDATE KB
        # -------------------------------------------------

        print("\n[STEP 1] Validating KB...\n")

        validation_report = (
            self.validator.validate()
        )

        print_validation_report(
            validation_report
        )

        if not validation_report.valid:

            print("\n[PIPELINE STOPPED]")
            print(
                "KB validation failed."
            )

            return
        
        # -------------------------------------------------
        # STEP 2 — LOAD PRODUCT METADATA
        # -------------------------------------------------

        print("\n[STEP 2] Loading Product Metadata...\n")

        metadata_objects = self.metadata_loader.load()

        metadata_lookup = {
            metadata.product_id: metadata.metadata
            for metadata in metadata_objects
        }

        # -------------------------------------------------
        # STEP 3 — LOAD DOCUMENTS
        # -------------------------------------------------

        print("\n[STEP 3] Loading Documents...\n")

        documents = self.loader.load()

        print(
            f"Loaded {len(documents)} documents."
        )

        # -------------------------------------------------
        # PIPELINE STATISTICS
        # -------------------------------------------------

        total_sections = 0

        total_chunks = 0

        # -------------------------------------------------
        # STEP 4 — PROCESS DOCUMENTS
        # -------------------------------------------------

        print("\n[STEP 4] Processing Documents...\n")

        for i, document in enumerate(documents, start=1):

            print(
                f"[{i}/{len(documents)}] "
                f"{document.product_id} "
                f"→ {document.file_type}"
            )

            # -------------------------------------------------
            # Enrich document with metadata
            # -------------------------------------------------
            product_metadata = metadata_lookup.get(
                document.product_id,
                {}
            )

            base_metadata = {

                "product_id": document.product_id,

                "category": document.category,

                "source_file": f"{document.file_type}.md",

                "visibility": product_metadata.get(
                    "visibility"
                ),

                "status": product_metadata.get(
                    "status"
                ),

                "aliases": product_metadata.get(
                    "aliases", []
                ),

                "tags": product_metadata.get(
                    "tags", []
                ),

                "retrieval_priority": (
                    product_metadata
                    .get("retrieval", {})
                    .get("priority", 0.5)
                ),
            }

            # ---------------------------------------------
            # Parse Sections
            # ---------------------------------------------

            parsed_sections = self.parser.parse(
                document.content
            )

            total_sections += len(
                parsed_sections
            )

            # ---------------------------------------------
            # Persist Parsed Artifacts
            # ---------------------------------------------

            self.artifact_writer.write_parsed_sections(

                sections=parsed_sections,

                category=document.category,

                product_id=document.product_id,

                source_file=document.file_type,
            )

            # ---------------------------------------------
            # Normalize Sections
            # ---------------------------------------------

            normalized_sections = (
                self.normalizer.normalize_sections(
                    parsed_sections
                )
            )

            # ---------------------------------------------
            # Persist Normalized Artifacts
            # ---------------------------------------------

            self.artifact_writer.write_normalized_sections(

                sections=normalized_sections,

                category=document.category,

                product_id=document.product_id,

                source_file=document.file_type,
            )

            # ---------------------------------------------
            # Generate Chunks
            # ---------------------------------------------

            chunks = self.chunker.chunk_sections(

                sections=normalized_sections,
                base_metadata = base_metadata
            )

            total_chunks += len(chunks)

            # ---------------------------------------------
            # Persist Chunk Artifacts
            # ---------------------------------------------

            self.artifact_writer.write_chunks(

                chunks=chunks,

                category=document.category,

                product_id=document.product_id,

                source_file=document.file_type,
            )

        # -------------------------------------------------
        # STEP 5 — PIPELINE SUMMARY
        # -------------------------------------------------

        self._print_pipeline_summary(

            documents=documents,

            total_sections=total_sections,

            total_chunks=total_chunks,
        )

        # -------------------------------------------------
        # STEP 6 — WRITE PIPELINE LOG
        # -------------------------------------------------

        self.artifact_writer.write_pipeline_log({

            "documents_processed": (
                len(documents)
            ),

            "sections_generated": (
                total_sections
            ),

            "chunks_generated": (
                total_chunks
            ),

            "status": "success",
        })

        print("\n[PIPELINE COMPLETED SUCCESSFULLY]")

    # -----------------------------------------------------

    def _print_pipeline_header(
        self
    ):

        print("\n" + "=" * 70)
        print("HASANAH MART INGESTION PIPELINE")
        print("=" * 70)

        print(f"\nKB Root:")
        print(self.kb_root)

    # -----------------------------------------------------

    def _print_pipeline_summary(
        self,
        documents,
        total_sections,
        total_chunks,
    ):

        print("\n" + "=" * 70)
        print("PIPELINE SUMMARY")
        print("=" * 70)

        print(
            f"\nDocuments Processed : "
            f"{len(documents)}"
        )

        print(
            f"Sections Generated  : "
            f"{total_sections}"
        )

        print(
            f"Chunks Generated    : "
            f"{total_chunks}"
        )

        # -------------------------------------------------
        # Category Distribution
        # -------------------------------------------------

        category_counter = Counter(

            doc.category
            for doc in documents
        )

        print("\nCategory Distribution:")

        for category, count in sorted(
            category_counter.items()
        ):

            print(
                f"  - {category}: {count}"
            )

        # -------------------------------------------------
        # File Type Distribution
        # -------------------------------------------------

        file_type_counter = Counter(

            doc.file_type
            for doc in documents
        )

        print("\nFile Type Distribution:")

        for file_type, count in sorted(
            file_type_counter.items()
        ):

            print(
                f"  - {file_type}: {count}"
            )

        print("\nArtifacts Written To:")

        print("  artifacts/parsed/")
        print("  artifacts/normalized/")
        print("  artifacts/chunked/")
        print("  artifacts/pipeline_logs/")


# ---------------------------------------------------------
# MAIN EXECUTION
# ---------------------------------------------------------

if __name__ == "__main__":

    pipeline = IngestionPipeline(

        kb_root=(
            "knowledge_base"
        )
    )

    pipeline.run()