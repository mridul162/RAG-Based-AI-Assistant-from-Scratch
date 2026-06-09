from pathlib import Path
import yaml
from itertools import combinations


ROOT_DIR = Path("knowledge_base/catalog/products")


# Optional keyword normalization
STOPWORDS = {
    "flower",
    "pure",
    "raw",
    "natural"
}


def clean_text(text: str) -> str:

    return (
        text.lower()
        .replace("-", " ")
        .replace("_", " ")
        .strip()
    )


def generate_token_aliases(tokens: list[str]) -> set[str]:

    aliases = set()

    # Full phrase
    aliases.add(" ".join(tokens))

    # Partial combinations
    for r in range(2, len(tokens)):

        for combo in combinations(tokens, r):

            aliases.add(" ".join(combo))

    return aliases


def generate_aliases(
    product_id: str,
    en_name: str,
    bn_name: str
) -> list[str]:

    aliases = set()

    # -------------------------
    # Product ID aliases
    # -------------------------

    cleaned_product_id = clean_text(product_id)

    aliases.add(cleaned_product_id)

    # -------------------------
    # English aliases
    # -------------------------

    cleaned_en = clean_text(en_name)

    aliases.add(cleaned_en)

    en_tokens = [
        token
        for token in cleaned_en.split()
        if token not in STOPWORDS
    ]

    aliases.update(
        generate_token_aliases(en_tokens)
    )

    # -------------------------
    # Bengali aliases
    # -------------------------

    cleaned_bn = bn_name.strip()

    if cleaned_bn:

        aliases.add(cleaned_bn)

        bn_tokens = cleaned_bn.split()

        aliases.update(
            generate_token_aliases(bn_tokens)
        )

    # -------------------------
    # Remove invalid aliases
    # -------------------------

    cleaned_aliases = {
        alias.strip()
        for alias in aliases
        if alias.strip()
    }

    return sorted(cleaned_aliases)


yaml_files = ROOT_DIR.rglob("product.yaml")


for yaml_file in yaml_files:

    with open(yaml_file, "r", encoding="utf-8") as f:
        metadata = yaml.safe_load(f)

    product_id = metadata.get("product_id", "")
    en_name = metadata.get("name", {}).get("en", "")
    bn_name = metadata.get("name", {}).get("bn", "")

    aliases = generate_aliases(
        product_id=product_id,
        en_name=en_name,
        bn_name=bn_name
    )

    metadata["aliases"] = aliases

    with open(yaml_file, "w", encoding="utf-8") as f:

        yaml.dump(
            metadata,
            f,
            allow_unicode=True,
            sort_keys=False
        )

    print(f"[UPDATED] {yaml_file}")
    print(f"Generated {len(aliases)} aliases")