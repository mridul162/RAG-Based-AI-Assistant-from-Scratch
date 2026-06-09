from pathlib import Path
from datetime import date
import yaml
from slugify import slugify

ROOT_DIR = Path("knowledge_base/catalog/products")

DEFAULT_TEMPLATE = {
    "schema_version": 1,

    "product_id": "",
    "slug": "",

    "name": {
        "bn": "",
        "en": ""
    },

    "category": "",
    "subcategory": "",

    "status": "active",
    "visibility": "public",

    "origin": {
        "region": "",
        "country": "Bangladesh"
    },

    "availability": {
        "seasonal": False
    },

    "pricing": {
        "currency": "BDT"
    },

    "languages_supported": [
        "bn",
        "en",
        "banglish"
    ],

    "aliases": [],
    "tags": [],

    "embedding_context": "",

    "retrieval": {
        "priority": 0.90,
        "business_critical": True,
        "boost_terms": []
    },

    "content_defaults": {
        "primary_language": "bn",
        "fallback_language": "en"
    },

    "updated_at": str(date.today())
}


def add_semantic_spacing(yaml_text: str) -> str:

    sections = [
        "product_id:",
        "name:",
        "category:",
        "status:",
        "origin:",
        "availability:",
        "pricing:",
        "languages_supported:",
        "aliases:",
        "embedding_context:",
        "retrieval:",
        "content_defaults:",
        "updated_at:"
    ]

    lines = yaml_text.splitlines()
    output = []

    for line in lines:

        for section in sections:
            if line.startswith(section):
                output.append("")

        output.append(line)

    return "\n".join(output).strip() + "\n"


yaml_files = ROOT_DIR.rglob("product.yaml")

for yaml_file in yaml_files:

    product_folder = yaml_file.parent
    category = product_folder.parent.name
    product_id = product_folder.name

    metadata = DEFAULT_TEMPLATE.copy()

    metadata["product_id"] = product_id
    metadata["slug"] = slugify(product_id)
    metadata["category"] = category

    inferred_name = product_id.replace("_", " ").title()

    metadata["name"]["en"] = inferred_name

    metadata["tags"] = [category]

    metadata["retrieval"]["boost_terms"] = sorted({
        inferred_name.lower(),
        product_id.replace("_", " ")
    })

    yaml_content = yaml.dump(
        metadata,
        allow_unicode=True,
        sort_keys=False
    )

    yaml_content = add_semantic_spacing(yaml_content)

    with open(yaml_file, "w", encoding="utf-8") as f:
        f.write(yaml_content)

    print(f"[UPDATED] {yaml_file}")