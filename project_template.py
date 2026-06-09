from pathlib import Path

PROJECT_NAME = "RAG-System-from-Scratch"

# =========================================================
# PROJECT STRUCTURE
# =========================================================

project_structure = [

    # =====================================================
    # API LAYER
    # =====================================================

    "api/core",
    "api/routes",
    "api/services",
    "api/schemas",
    "api/db",
    "api/dependencies",
    "api/middleware",
    "api/utils",

    # =====================================================
    # FRONTEND
    # =====================================================

    "frontend",

    # =====================================================
    # KNOWLEDGE BASE
    # =====================================================

    "knowledge_base/catalog/products/honey",
    "knowledge_base/catalog/products/ghee",
    "knowledge_base/catalog/products/dates",
    "knowledge_base/catalog/products/nuts",
    "knowledge_base/catalog/products/oils",
    "knowledge_base/catalog/products/fruits",
    "knowledge_base/catalog/products/seeds",

    "knowledge_base/catalog/categories",
    "knowledge_base/catalog/bundles",
    "knowledge_base/catalog/comparisons",

    "knowledge_base/global/company",
    "knowledge_base/global/customer_support",
    "knowledge_base/global/conversational",
    "knowledge_base/global/health",
    "knowledge_base/global/multilingual",
    "knowledge_base/global/system",

    "knowledge_base/taxonomy",
    "knowledge_base/schemas",

    # =====================================================
    # INGESTION PIPELINE
    # =====================================================

    "ingestion/raw",
    "ingestion/cleaned",
    "ingestion/normalized",
    "ingestion/chunked",
    "ingestion/embeddings/faiss",
    "ingestion/embeddings/metadata",
    "ingestion/embeddings/snapshots",
    "ingestion/pipeline_logs",

    # =====================================================
    # EVALUATION
    # =====================================================

    "evaluation/retrieval",
    "evaluation/hallucination",
    "evaluation/prompting",
    "evaluation/analytics",

    # =====================================================
    # PROMPTS
    # =====================================================

    "prompts/system",
    "prompts/retrieval",
    "prompts/evaluation",

    # =====================================================
    # VECTOR DATABASE
    # =====================================================

    "vector_db",

    # =====================================================
    # LOGS
    # =====================================================

    "logs",

    # =====================================================
    # NOTEBOOKS
    # =====================================================

    "notebooks",

    # =====================================================
    # SCRIPTS
    # =====================================================

    "scripts",

    # =====================================================
    # ENGINEERING DOCUMENTATION
    # =====================================================

    "engineering_docs",
]


# =========================================================
# FILES TO CREATE
# =========================================================

files_to_create = [

    # =====================================================
    # ROOT FILES
    # =====================================================

    ".env",
    ".gitignore",
    ".dockerignore",
    "README.md",
    "requirements.txt",
    "Dockerfile",
    "render.yaml",

    # =====================================================
    # API FILES
    # =====================================================

    "api/__init__.py",
    "api/app.py",

    "api/core/__init__.py",
    "api/core/config.py",
    "api/core/logging.py",

    "api/routes/__init__.py",
    "api/routes/chat.py",
    "api/routes/whatsapp.py",
    "api/routes/dashboard.py",

    "api/services/__init__.py",
    "api/services/rag_service.py",
    "api/services/embedding_service.py",
    "api/services/retrieval_service.py",
    "api/services/whatsapp_service.py",

    "api/schemas/__init__.py",
    "api/schemas/chat_schema.py",

    "api/db/__init__.py",
    "api/db/database.py",
    "api/db/models.py",
    "api/db/crud.py",

    "api/dependencies/__init__.py",

    # =====================================================
    # FRONTEND FILES
    # =====================================================

    "frontend/app.py",

    # =====================================================
    # ENGINEERING DOCS
    # =====================================================

    "engineering_docs/PROJECT_CONTEXT.md",
    "engineering_docs/SYSTEM_ARCHITECTURE.md",
    "engineering_docs/DECISIONS_LOG.md",
    "engineering_docs/KB_DESIGN.md",
    "engineering_docs/CHUNKING_STRATEGY.md",
    "engineering_docs/RETRIEVAL_STRATEGY.md",
    "engineering_docs/MULTILINGUAL_STRATEGY.md",
    "engineering_docs/EVALUATION_STRATEGY.md",

    # =====================================================
    # TAXONOMY FILES
    # =====================================================

    "knowledge_base/taxonomy/product_categories.yaml",
    "knowledge_base/taxonomy/knowledge_types.yaml",
    "knowledge_base/taxonomy/intent_types.yaml",
    "knowledge_base/taxonomy/retrieval_priorities.yaml",
    "knowledge_base/taxonomy/multilingual_aliases.yaml",

    # =====================================================
    # SCHEMA FILES
    # =====================================================

    "knowledge_base/schemas/product_schema.json",
    "knowledge_base/schemas/metadata_schema.json",
    "knowledge_base/schemas/chunk_schema.json",
    "knowledge_base/schemas/retrieval_schema.json",

    # =====================================================
    # PROMPTS
    # =====================================================

    "prompts/system/base_system_prompt.md",
    "prompts/system/whatsapp_prompt.md",
    "prompts/system/sales_prompt.md",

    "prompts/retrieval/retrieval_prompt.md",
    "prompts/retrieval/reranking_prompt.md",
    "prompts/retrieval/grounding_prompt.md",

    "prompts/evaluation/evaluation_prompt.md",
    "prompts/evaluation/hallucination_detection.md",

    # =====================================================
    # EVALUATION FILES
    # =====================================================

    "evaluation/retrieval/benchmark_queries.md",
    "evaluation/retrieval/retrieval_failures.md",
    "evaluation/retrieval/multilingual_tests.md",
    "evaluation/retrieval/ranking_analysis.md",

    "evaluation/hallucination/hallucination_cases.md",
    "evaluation/hallucination/grounding_failures.md",

    "evaluation/prompting/prompt_versions.md",
    "evaluation/prompting/response_quality.md",

    "evaluation/analytics/user_query_patterns.md",
    "evaluation/analytics/failed_queries.md",

    # =====================================================
    # VECTOR DB PLACEHOLDERS
    # =====================================================

    "vector_db/.gitkeep",

    # =====================================================
    # LOGS PLACEHOLDERS
    # =====================================================

    "logs/.gitkeep",
]


# =========================================================
# CREATE PROJECT STRUCTURE
# =========================================================

def create_structure():
    root = Path("./")

    # Create directories
    for folder in project_structure:
        folder_path = root / folder
        folder_path.mkdir(parents=True, exist_ok=True)

    # Create files
    for file in files_to_create:
        file_path = root / file

        file_path.parent.mkdir(parents=True, exist_ok=True)

        if not file_path.exists():
            file_path.touch()

    print(f"\n✅ Project structure created successfully.")
    print(f"📁 Root directory: {root.resolve()}")


# =========================================================
# MAIN
# =========================================================

if __name__ == "__main__":
    create_structure()