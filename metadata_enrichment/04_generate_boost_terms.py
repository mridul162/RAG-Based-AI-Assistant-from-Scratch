from pathlib import Path
import yaml


ROOT_DIR = Path("knowledge_base/catalog/products")


# Terms that usually do not help retrieval strongly
LOW_SIGNAL_WORDS = {
    "product",
    "food",
    "organic",
    "natural",
    "pure"
}


def normalize(text: str) -> str:

    return (
        text.lower()
        .replace("-", " ")
        .replace("_", " ")
        .strip()
    )


def generate_boost_terms(
    product_id: str,
    en_name: str,
    bn_name: str,
    aliases: list[str],
    category: str
) -> list[str]:

    boost_terms = set()

    # -------------------------
    # Product ID
    # -------------------------

    boost_terms.add(
        normalize(product_id)
    )

    # -------------------------
    # English name
    # -------------------------

    normalized_en = normalize(en_name)

    boost_terms.add(normalized_en)

    # -------------------------
    # Bengali name
    # -------------------------

    if bn_name.strip():

        boost_terms.add(
            bn_name.strip()
        )

    # -------------------------
    # Category
    # -------------------------

    if category.strip():

        boost_terms.add(
            normalize(category)
        )

    # -------------------------
    # Alias enrichment
    # -------------------------

    for alias in aliases:

        cleaned_alias = normalize(alias)

        if not cleaned_alias:
            continue

        # Avoid noisy single-token aliases
        if len(cleaned_alias.split()) < 2:
            continue

        boost_terms.add(cleaned_alias)

    # -------------------------
    # Remove weak/noisy terms
    # -------------------------

    final_terms = set()

    for term in boost_terms:

        tokens = term.split()

        filtered_tokens = [
            token
            for token in tokens
            if token not in LOW_SIGNAL_WORDS
        ]

        cleaned_term = " ".join(filtered_tokens).strip()

        if cleaned_term:
            final_terms.add(cleaned_term)

    return sorted(final_terms)


yaml_files = ROOT_DIR.rglob("product.yaml")


for yaml_file in yaml_files:

    with open(yaml_file, "r", encoding="utf-8") as f:
        metadata = yaml.safe_load(f)

    product_id = metadata.get("product_id", "")

    en_name = metadata.get(
        "name", {}
    ).get("en", "")

    bn_name = metadata.get(
        "name", {}
    ).get("bn", "")

    aliases = metadata.get(
        "aliases", []
    )

    category = metadata.get(
        "category", ""
    )

    boost_terms = generate_boost_terms(
        product_id=product_id,
        en_name=en_name,
        bn_name=bn_name,
        aliases=aliases,
        category=category
    )

    # Ensure retrieval object exists
    if "retrieval" not in metadata:
        metadata["retrieval"] = {}

    metadata["retrieval"]["boost_terms"] = boost_terms

    with open(yaml_file, "w", encoding="utf-8") as f:

        yaml.dump(
            metadata,
            f,
            allow_unicode=True,
            sort_keys=False
        )

    print(f"[UPDATED] {yaml_file}")
    print(f"Generated {len(boost_terms)} boost terms")