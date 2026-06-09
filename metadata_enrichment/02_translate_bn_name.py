from pathlib import Path
import yaml
from deep_translator import GoogleTranslator


ROOT_DIR = Path("knowledge_base/catalog/products")


def translate_to_bengali(text: str) -> str:

    if not text or not text.strip():
        return ""

    try:
        return GoogleTranslator(
            source="en",
            target="bn"
        ).translate(text)

    except Exception as e:
        print(f"[FAILED] {text} -> {e}")
        return ""


yaml_files = ROOT_DIR.rglob("product.yaml")


for yaml_file in yaml_files:

    with open(yaml_file, "r", encoding="utf-8") as f:
        metadata = yaml.safe_load(f)

    en_name = metadata.get("name", {}).get("en", "").strip()
    bn_name = metadata.get("name", {}).get("bn", "").strip()

    # Skip if Bengali name already exists
    if bn_name:
        print(f"[SKIPPED] Bengali already exists -> {yaml_file}")
        continue

    translated_name = translate_to_bengali(en_name)

    metadata["name"]["bn"] = translated_name

    with open(yaml_file, "w", encoding="utf-8") as f:
        yaml.dump(
            metadata,
            f,
            allow_unicode=True,
            sort_keys=False
        )

    print(f"[UPDATED] {yaml_file}")
    print(f"  EN: {en_name}")
    print(f"  BN: {translated_name}")