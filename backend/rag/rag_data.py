import json
from pathlib import Path

from rag.vector_store import load_index


INDEX_DIR = Path(__file__).parent / "index"


# --------------------------------------------------
# Load FAISS index
# --------------------------------------------------

index = load_index(
    INDEX_DIR / "faiss.index"
)


# --------------------------------------------------
# Load metadata
# --------------------------------------------------

with open(
    INDEX_DIR / "metadata.json",
    "r",
    encoding="utf-8"
) as f:

    metadata = json.load(f)


# --------------------------------------------------
# Load chunks
# --------------------------------------------------

with open(
    INDEX_DIR / "chunks.json",
    "r",
    encoding="utf-8"
) as f:

    all_chunks = json.load(f)


# --------------------------------------------------
# Verification
# --------------------------------------------------

print("Loaded vectors:", index.ntotal)
print("Loaded chunks:", len(all_chunks))
print("Loaded metadata:", len(metadata))