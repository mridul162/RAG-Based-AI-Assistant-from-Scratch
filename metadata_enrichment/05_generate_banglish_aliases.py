from pathlib import Path
from itertools import combinations
import re
import yaml


ROOT_DIR = Path("knowledge_base/catalog/products")


# --------------------------------------------------
# Optional stopwords
# --------------------------------------------------

STOPWORDS = {
    "flower",
    "pure",
    "raw",
    "natural"
}


# --------------------------------------------------
# Bangladesh-style Banglish mappings
# --------------------------------------------------

WORD_MAP = {
    "মধু": "modhu",
    "ফুল": "ful",
    "ফুলের": "fuler",
    "খলিশা": "kholisha",
    "সরিষা": "sorisha",
    "সরিষার": "sorishar",
    "ঘি": "ghee",
    "দেশি": "deshi",
    "সুন্দরবন": "sundarban",
    "সুন্দরবনের": "sundarboner",
    "নারিকেল": "narikel",
    "তেল": "tel",
    "চাল": "chal",
    "ডাল": "dal",
    "গুড়": "gur",
    "খেজুর": "khejur",
    "বাদাম": "badam",
    "মসুর": "mosur",
    "কালোজিরা": "kalojira",
    "হলুদ": "holud",
    "আটা": "ata"
}


CHAR_MAP = {
    "অ": "o",
    "আ": "a",
    "ই": "i",
    "ঈ": "ee",
    "উ": "u",
    "ঊ": "oo",
    "এ": "e",
    "ঐ": "oi",
    "ও": "o",
    "ঔ": "ou",

    "ক": "k",
    "খ": "kh",
    "গ": "g",
    "ঘ": "gh",
    "ঙ": "ng",

    "চ": "ch",
    "ছ": "chh",
    "জ": "j",
    "ঝ": "jh",

    "ট": "t",
    "ঠ": "th",
    "ড": "d",
    "ঢ": "dh",

    "ত": "t",
    "থ": "th",
    "দ": "d",
    "ধ": "dh",
    "ন": "n",

    "প": "p",
    "ফ": "f",
    "ব": "b",
    "ভ": "bh",
    "ম": "m",

    "য": "j",
    "য়": "y",
    "র": "r",
    "ল": "l",

    "শ": "sh",
    "ষ": "sh",
    "স": "s",
    "হ": "h",

    "া": "a",
    "ি": "i",
    "ী": "ee",
    "ু": "u",
    "ূ": "oo",
    "ে": "e",
    "ৈ": "oi",
    "ো": "o",
    "ৌ": "ou",

    "ং": "ng",
    "ঃ": "h",
    "ঁ": "n",

    " ": " "
}


# --------------------------------------------------
# Cleanup rules
# --------------------------------------------------

REPLACEMENTS = [
    ("aa", "a"),
    ("ee", "i"),
    ("oo", "u"),
    ("ou", "o")
]


# --------------------------------------------------
# Utility functions
# --------------------------------------------------

def clean_text(text: str) -> str:

    return (
        text.lower()
        .replace("-", " ")
        .replace("_", " ")
        .strip()
    )


def transliterate_word(word: str) -> str:

    if word in WORD_MAP:
        return WORD_MAP[word]

    transliterated = ""

    for char in word:

        transliterated += CHAR_MAP.get(char, char)

    for old, new in REPLACEMENTS:

        transliterated = transliterated.replace(old, new)

    return transliterated


def generate_banglish(text: str) -> str:

    text = text.strip()

    if not text:
        return ""

    words = re.split(r"\s+", text)

    banglish_words = [
        transliterate_word(word)
        for word in words
    ]

    return " ".join(banglish_words).strip().lower()


def generate_token_aliases(tokens: list[str]) -> set[str]:

    aliases = set()

    # Full phrase
    aliases.add(" ".join(tokens))

    # Partial combinations
    for r in range(2, len(tokens)):

        for combo in combinations(tokens, r):

            aliases.add(" ".join(combo))

    return aliases


# --------------------------------------------------
# Main alias generator
# --------------------------------------------------

def generate_aliases(
    product_id: str,
    en_name: str,
    bn_name: str
) -> list[str]:

    aliases = set()

    # ------------------------------------------
    # Product ID aliases
    # ------------------------------------------

    cleaned_product_id = clean_text(product_id)

    aliases.add(cleaned_product_id)

    # ------------------------------------------
    # English aliases
    # ------------------------------------------

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

    # ------------------------------------------
    # Bengali aliases
    # ------------------------------------------

    cleaned_bn = bn_name.strip()

    if cleaned_bn:

        aliases.add(cleaned_bn)

        bn_tokens = cleaned_bn.split()

        aliases.update(
            generate_token_aliases(bn_tokens)
        )

    # ------------------------------------------
    # Banglish aliases
    # ------------------------------------------

    banglish_text = generate_banglish(
        cleaned_bn
    )

    if banglish_text:

        aliases.add(banglish_text)

        banglish_tokens = banglish_text.split()

        aliases.update(
            generate_token_aliases(
                banglish_tokens
            )
        )

    # ------------------------------------------
    # Final cleanup
    # ------------------------------------------

    cleaned_aliases = {
        alias.strip().lower()
        for alias in aliases
        if alias.strip()
    }

    return sorted(cleaned_aliases)


# --------------------------------------------------
# Process all YAML files
# --------------------------------------------------

yaml_files = ROOT_DIR.rglob("product.yaml")


for yaml_file in yaml_files:

    with open(yaml_file, "r", encoding="utf-8") as f:

        metadata = yaml.safe_load(f)

    product_id = metadata.get(
        "product_id", ""
    )

    en_name = metadata.get(
        "name", {}
    ).get("en", "")

    bn_name = metadata.get(
        "name", {}
    ).get("bn", "")

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