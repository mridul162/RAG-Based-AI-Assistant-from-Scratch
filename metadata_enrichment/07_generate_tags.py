from pathlib import Path
import yaml


ROOT_DIR = Path("knowledge_base/catalog/products")


# --------------------------------------------------
# Generic low-signal words
# --------------------------------------------------

STOPWORDS = {
    "flower",
    "pure",
    "raw",
    "natural",
    "organic",
    "premium"
}


# --------------------------------------------------
# Normalize text
# --------------------------------------------------

def normalize(text: str) -> str:

    return (
        text.lower()
        .replace("-", " ")
        .replace("_", " ")
        .strip()
    )


# --------------------------------------------------
# Generate tags
# --------------------------------------------------

def generate_tags(
    category: str,
    subcategory: str,
    en_name: str,
    bn_name: str,
    aliases: list[str]
) -> list[str]:

    tags = set()

    # ------------------------------------------
    # Category + subcategory
    # ------------------------------------------

    if category.strip():
        tags.add(
            normalize(category)
        )

    if subcategory.strip():
        tags.add(
            normalize(subcategory)
        )

    # ------------------------------------------
    # English keywords
    # ------------------------------------------

    en_tokens = [
        token
        for token in normalize(en_name).split()
        if token not in STOPWORDS
    ]

    tags.update(en_tokens)

    # ------------------------------------------
    # Bengali keywords
    # ------------------------------------------

    bn_tokens = bn_name.split()

    tags.update([
        token.strip()
        for token in bn_tokens
        if token.strip()
    ])

    # ------------------------------------------
    # High-signal aliases only
    # ------------------------------------------

    for alias in aliases:

        cleaned_alias = normalize(alias)

        # Avoid huge phrases
        if len(cleaned_alias.split()) > 3:
            continue

        # Avoid very short aliases
        if len(cleaned_alias) < 4:
            continue

        tags.add(cleaned_alias)

    # ------------------------------------------
    # Cleanup
    # ------------------------------------------

    final_tags = {
        tag.strip()
        for tag in tags
        if tag.strip()
    }

    return sorted(final_tags)


# --------------------------------------------------
# Process all YAML files
# --------------------------------------------------

yaml_files = ROOT_DIR.rglob("product.yaml")


for yaml_file in yaml_files:

    with open(yaml_file, "r", encoding="utf-8") as f:

        metadata = yaml.safe_load(f)

    category = metadata.get(
        "category", ""
    )

    subcategory = metadata.get(
        "subcategory", ""
    )

    en_name = metadata.get(
        "name", {}
    ).get("en", "")

    bn_name = metadata.get(
        "name", {}
    ).get("bn", "")

    aliases = metadata.get(
        "aliases", []
    )

    tags = generate_tags(
        category=category,
        subcategory=subcategory,
        en_name=en_name,
        bn_name=bn_name,
        aliases=aliases
    )

    metadata["tags"] = tags

    with open(yaml_file, "w", encoding="utf-8") as f:

        yaml.dump(
            metadata,
            f,
            allow_unicode=True,
            sort_keys=False
        )

    print(f"[UPDATED] {yaml_file}")
    print(f"Generated {len(tags)} tags")