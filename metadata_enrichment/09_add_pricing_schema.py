from pathlib import Path
from datetime import date
import yaml


ROOT_DIR = Path("knowledge_base/catalog/products")


# --------------------------------------------------
# Default pricing schema
# --------------------------------------------------

DEFAULT_PRICING = {
    "currency": "BDT",

    "updated_at": str(date.today()),

    "note": "Subject to seasonal change.",

    "variants": [
        {
            "label": "250g",
            "size_gm": 250,
            "price": 0,
            "in_stock": True
        },
        {
            "label": "500g",
            "size_gm": 500,
            "price": 0,
            "in_stock": True
        },
        {
            "label": "1kg",
            "size_gm": 1000,
            "price": 0,
            "in_stock": True
        }
    ]
}


# --------------------------------------------------
# Optional semantic YAML spacing
# --------------------------------------------------

SECTIONS = [
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


def add_semantic_spacing(yaml_text: str) -> str:

    lines = yaml_text.splitlines()

    output = []

    for line in lines:

        stripped = line.strip()

        for section in SECTIONS:

            if stripped.startswith(section):

                if output and output[-1] != "":
                    output.append("")

                break

        output.append(line)

    return "\n".join(output).strip() + "\n"


# --------------------------------------------------
# Process all product.yaml files
# --------------------------------------------------

yaml_files = ROOT_DIR.rglob("product.yaml")


for yaml_file in yaml_files:

    with open(yaml_file, "r", encoding="utf-8") as f:

        metadata = yaml.safe_load(f)

    # ------------------------------------------
    # Preserve existing prices if available
    # ------------------------------------------

    existing_pricing = metadata.get(
        "pricing", {}
    )

    existing_variants = existing_pricing.get(
        "variants", []
    )

    pricing = DEFAULT_PRICING.copy()

    # If variants already exist, preserve them
    if existing_variants:

        pricing["variants"] = existing_variants

    metadata["pricing"] = pricing

    # ------------------------------------------
    # Save YAML
    # ------------------------------------------

    yaml_content = yaml.dump(
        metadata,
        allow_unicode=True,
        sort_keys=False
    )

    yaml_content = add_semantic_spacing(
        yaml_content
    )

    with open(yaml_file, "w", encoding="utf-8") as f:

        f.write(yaml_content)

    print(f"[UPDATED] {yaml_file}")