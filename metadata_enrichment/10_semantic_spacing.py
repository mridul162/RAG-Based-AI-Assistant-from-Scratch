from pathlib import Path

ROOT_DIR = Path("knowledge_base/catalog/products")

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
        # Insert blank line before important sections
        for section in SECTIONS:
            if stripped.startswith(section):
                # Avoid duplicate empty lines
                if output and output[-1] != "":
                    output.append("")
                break
        output.append(line)

    return "\n".join(output).strip() + "\n"


yaml_files = ROOT_DIR.rglob("product.yaml")

for yaml_file in yaml_files:
    with open(yaml_file, "r", encoding="utf-8") as f:
        content = f.read()
    formatted_content = add_semantic_spacing(content)
    with open(yaml_file, "w", encoding="utf-8") as f:
        f.write(formatted_content)
    print(f"[FORMATTED] {yaml_file}")