from pathlib import Path


INGESTION_STRUCTURE = {
    "chunkers": [
        "__init__.py",
        "semantic_chunker.py"
    ],

    "embedders": [
        "__init__.py",
        "bge_embedder.py",
        "openai_embedder.py"
    ],

    "loaders": [
        "__init__.py",
        "markdown_loader.py",
        "product_metadata_loader.py"
    ],

    "models": [
        "__init__.py",
        "chunk_models.py",
        "document_models.py",
        "embedding_models.py",
        "parsed_models.py"
    ],

    "parsers": [
        "__init__.py",
        "markdown_parser.py"
    ],

    "pipelines": [
        "__init__.py",
        "build_vector_pipeline.py",
        "ingestion_pipeline.py"
    ],

    "utils": [
        "__init__.py",
        "artifact_writer.py",
        "logging_utils.py",
        "normalizer.py"
    ],

    "validators": [
        "__init__.py",
        "kb_validator.py"
    ],

    "vectorstores": [
        "__init__.py",
        "faiss_store.py"
    ]
}


def create_file(file_path: Path):
    """
    Create file if it does not exist.
    """

    file_path.parent.mkdir(parents=True, exist_ok=True)

    if not file_path.exists():
        file_path.touch()
        print(f"✅ Created: {file_path}")

    else:
        print(f"⚠️ Exists: {file_path}")


def create_ingestion_structure(base_path="."):

    ingestion_root = Path(base_path) / "ingestion"

    ingestion_root.mkdir(parents=True, exist_ok=True)

    create_file(ingestion_root / "__init__.py")

    for folder, files in INGESTION_STRUCTURE.items():

        folder_path = ingestion_root / folder
        folder_path.mkdir(parents=True, exist_ok=True)

        for filename in files:
            create_file(folder_path / filename)

    print("\n🎉 Ingestion structure created successfully.")


if __name__ == "__main__":
    create_ingestion_structure()