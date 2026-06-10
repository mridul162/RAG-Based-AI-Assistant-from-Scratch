from ingestion.utils.manifest_manager import (
    ManifestManager
)

manager = ManifestManager(
    "artifacts/embeddings/manifest.json"
)

manifest = manager.load()

print(manifest)

manager.save(
    {
        "test_product": "abc123"
    }
)