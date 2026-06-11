"""
semantic_chunker.py

Purpose:
--------
Convert parsed semantic sections into retrieval-optimized chunks.

Responsibilities:
-----------------
- Preserve semantic boundaries
- Preserve heading hierarchy
- Preserve table integrity
- Split oversized sections carefully
- Generate chunk metadata
- Produce embedding-ready chunk objects

This chunker DOES NOT:
----------------------
- generate embeddings
- tokenize using model tokenizers
- rerank chunks
- summarize content

Architecture Philosophy:
------------------------
Semantic coherence first.
Token optimization second.
"""

import re
import sys
import uuid

sys.stdout.reconfigure(encoding="utf-8")

from dataclasses import dataclass
from typing import Dict, Any, List, Optional


# ---------------------------------------------------------
# CHUNK MODEL
# ---------------------------------------------------------

@dataclass
class Chunk:
    """
    Retrieval-ready semantic chunk.
    """

    chunk_id: str
    text: str
    metadata: Dict[str, Any]


# ---------------------------------------------------------
# SEMANTIC CHUNKER
# ---------------------------------------------------------

class SemanticChunker:
    """
    Section-aware semantic chunker.
    """

    def __init__(
        self,
        target_size: int = 500,
        overlap_size: int = 75,
    ):

        self.target_size = target_size
        self.overlap_size = overlap_size

    # -----------------------------------------------------

    def chunk_sections(
        self,
        sections,
        base_metadata: Optional[Dict[str, Any]] = None,
    ) -> List[Chunk]:
        """
        Convert parsed sections into semantic chunks.
        """

        all_chunks = []

        for section_index, section in enumerate(sections):

            section_chunks = self._chunk_single_section(
                section=section,
                section_index=section_index,
                base_metadata=base_metadata or {},
            )

            all_chunks.extend(section_chunks)

        return all_chunks

    # -----------------------------------------------------

    def _chunk_single_section(
        self,
        section,
        section_index: int,
        base_metadata: Dict[str, Any],
    ) -> List[Chunk]:
        """
        Chunk a single semantic section.
        """

        section_text = self._build_section_text(
            section
        )

        word_count = self._estimate_word_count(
            section_text
        )

        # ---------------------------------------------
        # Preserve small semantic sections
        # ---------------------------------------------

        if word_count <= self.target_size:

            return [
                self._build_chunk(
                    text=section_text,
                    section=section,
                    chunk_index=0,
                    section_index=section_index,
                    base_metadata=base_metadata,
                )
            ]

        # ---------------------------------------------
        # Split oversized sections
        # ---------------------------------------------

        return self._split_large_section(
            section_text=section_text,
            section=section,
            section_index=section_index,
            base_metadata=base_metadata,
        )

    # -----------------------------------------------------

    def _build_section_text(
        self,
        section
    ) -> str:
        """
        Build retrieval-ready section text.

        Preserve:
        - headings
        - tables
        - semantic context
        """

        return (
            f"{'#' * section.level} "
            f"{section.heading}\n\n"
            f"{section.content}"
        ).strip()

    # -----------------------------------------------------

    def _split_large_section(
        self,
        section_text: str,
        section,
        section_index: int,
        base_metadata: Dict[str, Any],
    ) -> List[Chunk]:
        """
        Split oversized section using paragraph grouping.
        """

        paragraphs = self._split_paragraphs(
            section_text
        )

        chunks = []

        current_chunk = []

        current_size = 0

        chunk_index = 0

        for paragraph in paragraphs:

            paragraph_size = self._estimate_word_count(
                paragraph
            )

            # -----------------------------------------
            # Preserve atomic tables
            # -----------------------------------------

            if self._is_table_block(paragraph):

                if current_chunk:

                    chunk_text = "\n\n".join(
                        current_chunk
                    )

                    chunks.append(

                        self._build_chunk(
                            text=chunk_text,
                            section=section,
                            chunk_index=chunk_index,
                            section_index=section_index,
                            base_metadata=base_metadata,
                        )
                    )

                    chunk_index += 1

                    current_chunk = []

                    current_size = 0

                chunks.append(

                    self._build_chunk(
                        text=paragraph,
                        section=section,
                        chunk_index=chunk_index,
                        section_index=section_index,
                        base_metadata=base_metadata,
                    )
                )

                chunk_index += 1

                continue

            # -----------------------------------------
            # Target size exceeded
            # -----------------------------------------

            if (
                current_size + paragraph_size >
                self.target_size
            ):

                chunk_text = "\n\n".join(
                    current_chunk
                )

                chunks.append(

                    self._build_chunk(
                        text=chunk_text,
                        section=section,
                        chunk_index=chunk_index,
                        section_index=section_index,
                        base_metadata=base_metadata,
                    )
                )

                chunk_index += 1

                # -------------------------------------
                # Add light overlap
                # -------------------------------------

                overlap = self._build_overlap(
                    current_chunk
                )

                current_chunk = overlap + [
                    paragraph
                ]

                current_size = self._estimate_word_count(
                    "\n\n".join(current_chunk)
                )

            else:

                current_chunk.append(paragraph)

                current_size += paragraph_size

        # ---------------------------------------------
        # Final chunk
        # ---------------------------------------------

        if current_chunk:

            chunk_text = "\n\n".join(
                current_chunk
            )

            chunks.append(

                self._build_chunk(
                    text=chunk_text,
                    section=section,
                    chunk_index=chunk_index,
                    section_index=section_index,
                    base_metadata=base_metadata,
                )
            )

        return chunks

    # -----------------------------------------------------

    def _split_paragraphs(
        self,
        text: str
    ) -> List[str]:
        """
        Split text into semantic paragraph blocks
        while preserving HTML tables atomically.
        """

        # -------------------------------------------------
        # STEP 1 — Extract HTML tables
        # -------------------------------------------------

        table_pattern = re.compile(
            r"<table.*?>.*?</table>",
            re.DOTALL | re.IGNORECASE
        )

        tables = {}

        def replace_table(match):

            placeholder = (
                f"__TABLE_{len(tables)}__"
            )

            tables[placeholder] = match.group(0)

            return placeholder

        text = table_pattern.sub(
            replace_table,
            text
        )

        # -------------------------------------------------
        # STEP 2 — Split paragraphs safely
        # -------------------------------------------------

        paragraphs = re.split(
            r"\n\s*\n",
            text
        )

        cleaned_paragraphs = []

        # -------------------------------------------------
        # STEP 3 — Restore tables
        # -------------------------------------------------

        for paragraph in paragraphs:

            paragraph = paragraph.strip()

            if not paragraph:
                continue

            for placeholder, table in tables.items():

                paragraph = paragraph.replace(
                    placeholder,
                    table
                )

            cleaned_paragraphs.append(
                paragraph
            )

        return cleaned_paragraphs

    # -----------------------------------------------------

    def _is_table_block(
        self,
        text: str
    ) -> bool:
        """
        Detect markdown or HTML tables.
        """

        stripped = text.strip()

        # Markdown table
        if stripped.startswith("|"):
            return True

        # HTML table
        if "<table" in stripped.lower():
            return True

        return False

    # -----------------------------------------------------

    def _build_overlap(
        self,
        paragraphs: List[str]
    ) -> List[str]:
        """
        Build light semantic overlap.
        """

        if not paragraphs:
            return []

        overlap = []

        current_size = 0

        for paragraph in reversed(paragraphs):

            size = self._estimate_word_count(
                paragraph
            )

            if (
                current_size + size >
                self.overlap_size
            ):
                break

            overlap.insert(0, paragraph)

            current_size += size

        return overlap

    # -----------------------------------------------------

    def _estimate_word_count(
        self,
        text: str
    ) -> int:
        """
        Lightweight word-count approximation.
        """

        return len(text.split())

    # -----------------------------------------------------

    def _build_chunk(
        self,
        text: str,
        section,
        chunk_index: int,
        section_index: int,
        base_metadata: Dict[str, Any],
    ) -> Chunk:
        """
        Build final chunk object.
        """

        chunk_id = (
            f"{base_metadata['product_id']}__"
            f"{base_metadata['source_file']}__"
            f"{section_index}__"
            f"{chunk_index}"
        )

        metadata = {

            # -----------------------------------------
            # Base metadata
            # -----------------------------------------

            **base_metadata,

            # -----------------------------------------
            # Section metadata
            # -----------------------------------------

            "heading": section.heading,

            "heading_path": (
                section.heading_path
            ),

            "section_id": (
                section.section_id
            ),

            "section_level": (
                section.level
            ),

            # -----------------------------------------
            # Chunk metadata
            # -----------------------------------------

            "chunk_index": chunk_index,

            "section_index": section_index,

            "word_count": (
                self._estimate_word_count(
                    text
                )
            ),
            "chunking_strategy": "hybrid",
        }

        return Chunk(
            chunk_id=chunk_id,
            text=text,
            metadata=metadata,
        )


# ---------------------------------------------------------
# SIMPLE TEST EXECUTION
# ---------------------------------------------------------

if __name__ == "__main__":

    @dataclass
    class ParsedSection:

        heading: str
        level: int
        content: str
        heading_path: List[str]
        section_id: Optional[str] = None

    sample_section = ParsedSection(

        heading="Our Prices",

        level=2,

        heading_path=[
            "Pricing",
            "Our Prices"
        ],

        section_id="our-prices",

        content="""
            <table>
            <thead>
            <tr>
            <th>Size</th>
            <th>Price</th>
            </tr>
            </thead>

            <tbody>
            <tr>
            <td>250g</td>
            <td>৳320</td>
            </tr>

            <tr>
            <td>500g</td>
            <td>৳600</td>
            </tr>
            </tbody>
            </table>

            Prices valid as of May 2026.

            The larger size offers better value for regular family usage.
            """ * 8
    )

    chunker = SemanticChunker(
        target_size=120,
        overlap_size=30,
    )

    chunks = chunker.chunk_sections(
        sections=[sample_section],

        base_metadata={
            "product_id": "kholisha_honey",
            "category": "honey",
            "source_file": "pricing.md",
        }
    )

    print("\n" + "=" * 70)
    print("SEMANTIC CHUNKER OUTPUT")
    print("=" * 70)

    print(f"\nGenerated Chunks: {len(chunks)}")

    for i, chunk in enumerate(chunks, start=1):

        print("\n" + "-" * 70)

        print(f"CHUNK #{i}")

        print("-" * 70)

        print(f"Chunk ID: {chunk.chunk_id}")

        print("\nMetadata:")

        for k, v in chunk.metadata.items():

            print(f"{k}: {v}")

        print("\nText Preview:")
        print(chunk.text[:700])