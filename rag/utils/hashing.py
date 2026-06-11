import hashlib
import json


def generate_product_hash(
    chunks: list[dict]
) -> str:
    """
    Generate deterministic hash for a product's chunks.
    """

    payload = json.dumps(
        chunks,
        sort_keys=True,
        ensure_ascii=False
    )

    return hashlib.sha256(
        payload.encode("utf-8")
    ).hexdigest()


if __name__ == "__main__":
    from rag.utils.hashing import (
        generate_product_hash
    )

    chunks = [
        {
            "chunk_id": "1",
            "text": "hello world"
        }
    ]

    print(
        generate_product_hash(chunks)
    )