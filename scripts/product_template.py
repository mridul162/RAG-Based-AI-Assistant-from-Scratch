from pathlib import Path
import argparse
import textwrap


# =========================================================
# PRODUCT TEMPLATE FILES
# =========================================================

ROOT_FILES = {
    "product.yaml": textwrap.dedent("""\
        schema_version: 1

        product_id:
        slug:

        name:
        bn:
        en:

        category:
        subcategory:

        status: active
        visibility: public

        origin:
        region:
        country: Bangladesh

        availability:
        seasonal: false

        pricing:
        currency: BDT

        languages_supported:
        - bn
        - en
        - banglish

        aliases: []

        tags: []

        embedding_context: ""

        retrieval:
        priority: 0.90
        business_critical: true
        boost_terms: []

        content_defaults:
        primary_language: bn
        fallback_language: en

        updated_at:
    """),

    "overview.md": "# Overview\n",
    "benefits.md": "# Benefits\n",
    "nutrition.md": "# Nutrition\n",
    "sourcing.md": "# Sourcing\n",
    "authenticity.md": "# Authenticity\n",
    "usage.md": "# Usage\n",
    "storage.md": "# Storage\n",
    "faq.md": "# FAQ\n",
    "warnings.md": "# Warnings\n",
    "comparisons.md": "# Comparisons\n",
    "pricing.md": "# Pricing\n",
    "shipping.md": "# Shipping\n",
    "aliases.md": "# Aliases\n",
}


QA_FILES = {
    "retrieval_queries.md": "# Retrieval Queries\n",
    "expected_answers.md": "# Expected Answers\n",
    "edge_cases.md": "# Edge Cases\n",
}


TRANSLATION_FILES = {
    "bn.md": "# Bengali Translation\n",
    "en.md": "# English Translation\n",
    "banglish.md": "# Banglish Translation\n",
}


MEDIA_FILES = [
    "hero.jpg",
    "raw.jpg",
]


# =========================================================
# CREATE FILE HELPER
# =========================================================

def create_file(path: Path, content: str = ""):
    """
    Create file if it does not exist.
    """

    path.parent.mkdir(parents=True, exist_ok=True)

    if not path.exists():
        path.write_text(content, encoding="utf-8")
        print(f"✅ Created file: {path}")
    else:
        print(f"⚠️ Already exists: {path}")


# =========================================================
# CREATE PRODUCT STRUCTURE
# =========================================================

def create_product_structure(
    base_path: str,
    category: str,
    product_name: str
):
    """
    Create canonical KB structure for a product.
    """

    product_path = (
        Path(base_path)
        / "catalog"
        / "products"
        / category
        / product_name
    )

    print("\n=================================================")
    print(f"Creating product structure for: {product_name}")
    print("=================================================\n")

    # -----------------------------------------------------
    # Root markdown + yaml files
    # -----------------------------------------------------

    for filename, content in ROOT_FILES.items():
        create_file(product_path / filename, content)

    # -----------------------------------------------------
    # QA directory
    # -----------------------------------------------------

    qa_path = product_path / "qa"

    for filename, content in QA_FILES.items():
        create_file(qa_path / filename, content)

    # -----------------------------------------------------
    # Translation directory
    # -----------------------------------------------------

    translation_path = product_path / "translations"

    for filename, content in TRANSLATION_FILES.items():
        create_file(translation_path / filename, content)

    # -----------------------------------------------------
    # Media directory
    # -----------------------------------------------------

    media_path = product_path / "media"

    media_path.mkdir(parents=True, exist_ok=True)

    for filename in MEDIA_FILES:
        create_file(media_path / filename)

    # Gallery folder
    gallery_path = media_path / "gallery"
    gallery_path.mkdir(parents=True, exist_ok=True)

    print(f"✅ Created directory: {gallery_path}")

    print("\n=================================================")
    print("🎉 Product KB structure created successfully.")
    print(f"📁 Location: {product_path.resolve()}")
    print("=================================================\n")


# =========================================================
# CLI
# =========================================================

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Create canonical product KB structure."
    )

    parser.add_argument(
        "--base-path",
        type=str,
        default="knowledge_base",
        help="Base knowledge base path"
    )

    parser.add_argument(
        "--category",
        type=str,
        required=True,
        help="Product category (e.g. honey)"
    )

    parser.add_argument(
        "--product",
        type=str,
        required=True,
        help="Product folder name"
    )

    args = parser.parse_args()

    create_product_structure(
        base_path=args.base_path,
        category=args.category,
        product_name=args.product
    )