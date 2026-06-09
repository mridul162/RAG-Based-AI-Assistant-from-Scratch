from pathlib import Path
import re
import yaml


ROOT_DIR = Path("knowledge_base/catalog/products")


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


REPLACEMENTS = [
    ("aa", "a"),
    ("ee", "i"),
    ("oo", "u"),
    ("ou", "o")
]


# --------------------------------------------------
# Utility functions
# --------------------------------------------------

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


def generate_banglish_boost_terms(
    bn_name: str
) -> list[str]:

    boost_terms = set()

    banglish_full = generate_banglish(
        bn_name
    )

    if not banglish_full:
        return []

    boost_terms.add(banglish_full)

    tokens = banglish_full.split()

    # --------------------------------------------------
    # High-signal partial combinations only
    # --------------------------------------------------

    if len(tokens) >= 3:

        # Last 3 tokens
        boost_terms.add(
            " ".join(tokens[-3:])
        )

    if len(tokens) >= 2:

        # Last 2 tokens
        boost_terms.add(
            " ".join(tokens[-2:])
        )

    # --------------------------------------------------
    # Remove noisy short terms
    # --------------------------------------------------

    final_terms = {
        term.strip()
        for term in boost_terms
        if len(term.split()) >= 2
    }

    return sorted(final_terms)


# --------------------------------------------------
# Process all YAML files
# --------------------------------------------------

yaml_files = ROOT_DIR.rglob("product.yaml")


for yaml_file in yaml_files:

    with open(yaml_file, "r", encoding="utf-8") as f:

        metadata = yaml.safe_load(f)

    bn_name = metadata.get(
        "name", {}
    ).get("bn", "").strip()

    if not bn_name:

        print(f"[SKIPPED] No Bengali name -> {yaml_file}")
        continue

    banglish_boost_terms = (
        generate_banglish_boost_terms(
            bn_name
        )
    )

    # Ensure retrieval exists
    if "retrieval" not in metadata:
        metadata["retrieval"] = {}

    existing_terms = set(
        metadata["retrieval"].get(
            "boost_terms", []
        )
    )

    existing_terms.update(
        banglish_boost_terms
    )

    metadata["retrieval"]["boost_terms"] = sorted(
        existing_terms
    )

    with open(yaml_file, "w", encoding="utf-8") as f:

        yaml.dump(
            metadata,
            f,
            allow_unicode=True,
            sort_keys=False
        )

    print(f"[UPDATED] {yaml_file}")
    print(
        f"Generated {len(banglish_boost_terms)} Banglish boost terms"
    )