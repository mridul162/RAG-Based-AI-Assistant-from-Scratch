from pathlib import Path
import json
import tiktoken

# --------------------------------------------------
# CONFIG
# --------------------------------------------------

CHUNK_DIR = Path("artifacts/chunked")

MODEL_NAME = "text-embedding-3-small"

# --------------------------------------------------
# TOKENIZER
# --------------------------------------------------

encoding = tiktoken.encoding_for_model(MODEL_NAME)

# --------------------------------------------------
# STATS
# --------------------------------------------------

total_files = 0
total_chunks = 0
total_tokens = 0

token_counts = []

# --------------------------------------------------
# RECURSIVE JSON SCAN
# --------------------------------------------------

for file_path in CHUNK_DIR.rglob("*.json"):

    total_files += 1

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Skip empty files
    if not data:
        continue

    for chunk in data:

        text = chunk.get("text", "")

        token_count = len(
            encoding.encode(text)
        )

        total_chunks += 1
        total_tokens += token_count

        token_counts.append(token_count)

# --------------------------------------------------
# REPORT
# --------------------------------------------------

print("\n" + "=" * 60)
print("TOKEN REPORT")
print("=" * 60)

print(f"Files Processed : {total_files}")
print(f"Chunks          : {total_chunks}")
print(f"Total Tokens    : {total_tokens}")

if token_counts:

    print(f"Min Tokens      : {min(token_counts)}")
    print(f"Max Tokens      : {max(token_counts)}")
    print(
        f"Avg Tokens      : "
        f"{sum(token_counts)/len(token_counts):.2f}"
    )

    estimated_cost = (
        total_tokens / 1_000_000
    ) * 0.02

    print(
        f"Embedding Cost  : "
        f"${estimated_cost:.6f}"
    )

tiny = 0
small = 0
medium = 0
large = 0
x_large = 0

for t in token_counts:

    if t < 10:
        tiny += 1
    elif t < 50:
        small += 1
    elif t < 250:
        medium += 1
    elif t < 500:
        large += 1
    else:
        x_large += 1

print("\nChunk Distribution")
print(f"<10 tokens      : {tiny}")
print(f"<50 tokens      : {small}")
print(f"50-250 tokens   : {medium}")
print(f"250-500 tokens  : {large}")
print(f">500 tokens     : {x_large}")