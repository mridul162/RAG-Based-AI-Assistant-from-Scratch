from pathlib import Path
import yaml


ROOT_DIR = Path("knowledge_base/catalog/products")


# --------------------------------------------------
# Product nouns / semantic anchors
# Aliases or boost terms usually should contain one
# --------------------------------------------------

ANCHOR_TERMS = {
    # English
    "honey",
    "oil",
    "ghee",
    "rice",
    "dates",
    "salt",
    "pickle",

    # Bangla
    "মধু",
    "তেল",
    "ঘি",
    "চাল",
    "খেজুর",
    "লবণ",

    # Banglish
    "modhu",
    "tel",
    "ghee",
    "chal",
    "khejur"
}


# --------------------------------------------------
# Generic / weak terms
# --------------------------------------------------

GENERIC_TERMS = {
    "organic",
    "natural",
    "pure",
    "premium",
    "food",
    "healthy"
}


# --------------------------------------------------
# Tag stopwords
# --------------------------------------------------

TAG_STOPWORDS = {
    "fuler",
    "flower",
    "ফুলের",
    "sundarboner",
    "সুন্দরবনের"
}


# --------------------------------------------------
# Utility
# --------------------------------------------------

def normalize(text: str) -> str:

    return (
        text.lower()
        .replace("-", " ")
        .replace("_", " ")
        .strip()
    )


def contains_anchor_term(text: str) -> bool:

    tokens = set(text.split())

    return bool(tokens & ANCHOR_TERMS)


# --------------------------------------------------
# Alias refinement
# --------------------------------------------------

def refine_aliases(aliases: list[str]) -> list[str]:

    refined = set()

    for alias in aliases:

        alias = normalize(alias)

        # Skip empty
        if not alias:
            continue

        # Skip overly long aliases
        if len(alias.split()) > 5:
            continue

        # Keep only meaningful phrases
        if contains_anchor_term(alias):

            refined.add(alias)

    return sorted(refined)


# --------------------------------------------------
# Boost term refinement
# --------------------------------------------------

def refine_boost_terms(
    boost_terms: list[str]
) -> list[str]:

    refined = set()

    for term in boost_terms:

        term = normalize(term)

        if not term:
            continue

        # Remove generic single words
        if term in GENERIC_TERMS:
            continue

        # Avoid weak single-token boosts
        if len(term.split()) == 1:

            if term not in ANCHOR_TERMS:
                continue

        # Must contain strong semantic anchor
        if contains_anchor_term(term):

            refined.add(term)

    return sorted(refined)


# --------------------------------------------------
# Tag refinement
# --------------------------------------------------

def refine_tags(tags: list[str]) -> list[str]:

    refined = set()

    for tag in tags:

        tag = normalize(tag)

        if not tag:
            continue

        # Remove very long tags
        if len(tag.split()) > 2:
            continue

        # Remove noisy stopwords
        if tag in TAG_STOPWORDS:
            continue

        refined.add(tag)

    return sorted(refined)


# --------------------------------------------------
# Process YAML files
# --------------------------------------------------

yaml_files = ROOT_DIR.rglob("product.yaml")


for yaml_file in yaml_files:

    with open(yaml_file, "r", encoding="utf-8") as f:

        metadata = yaml.safe_load(f)

    # ------------------------------------------
    # Refine aliases
    # ------------------------------------------

    aliases = metadata.get("aliases", [])

    metadata["aliases"] = refine_aliases(
        aliases
    )

    # ------------------------------------------
    # Refine boost terms
    # ------------------------------------------

    retrieval = metadata.get(
        "retrieval", {}
    )

    boost_terms = retrieval.get(
        "boost_terms", []
    )

    metadata["retrieval"]["boost_terms"] = (
        refine_boost_terms(boost_terms)
    )

    # ------------------------------------------
    # Refine tags
    # ------------------------------------------

    tags = metadata.get("tags", [])

    metadata["tags"] = refine_tags(
        tags
    )

    # ------------------------------------------
    # Save
    # ------------------------------------------

    with open(yaml_file, "w", encoding="utf-8") as f:

        yaml.dump(
            metadata,
            f,
            allow_unicode=True,
            sort_keys=False
        )

    print(f"[REFINED] {yaml_file}")

    print(
        f"Aliases: {len(metadata['aliases'])}"
    )

    print(
        f"Tags: {len(metadata['tags'])}"
    )

    print(
        f"Boost Terms: "
        f"{len(metadata['retrieval']['boost_terms'])}"
    )