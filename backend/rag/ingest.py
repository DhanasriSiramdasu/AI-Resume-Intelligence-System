import json
from pathlib import Path
from services.rag_generator import ask_rag
from rag.retriever import retrieve
from rag.vector_store import create_index,save_index

DOCUMENT_DIR = Path(__file__).parent / "documents"

INDEX_DIR = Path(__file__).parent / "index"
INDEX_DIR.mkdir(exist_ok=True)

documents = []

for file in DOCUMENT_DIR.glob("*.txt"):
    text=file.read_text(encoding="utf-8").strip()

    if text:
        documents.append({
            "source":file.name,
            "text": text
        })

print("Documents ingested:",len(documents))

for document in documents:
    print(document["source"])


def chunk_text(text, chunk_size=500, overlap=50):
    paragraphs = [
        p.strip()
        for p in text.split("\n\n")
        if p.strip()
    ]
    chunks = []
    current = ""
    for paragraph in paragraphs:
        if len(current) + len(paragraph) + 1 <= chunk_size:
            current += paragraph + "\n\n"
        else:
            if current:
                chunks.append(current.strip())
            overlap_text = current[-overlap:] if current else ""
            current = overlap_text + paragraph + "\n\n"
    if current:
        chunks.append(current.strip())
    return chunks



# for testing 

# for document in documents:
#     chunks = chunk_text(document["text"])

#     print(
#         document["source"],
#         "->",
#         len(chunks),
#         "chunks"
#     )

all_chunks=[]
metadata=[]

for document in documents:
    chunks = chunk_text(document["text"])
    for chunk in chunks:
        all_chunks.append(chunk)
        metadata.append({
            "source":document["source"]
        })

from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

embeddings=model.encode(all_chunks)

index=create_index(embeddings)

save_index(index,INDEX_DIR/"faiss.index")

with open(INDEX_DIR / "metadata.json", "w", encoding="utf-8") as f:
    json.dump(metadata, f, indent=2)
with open(INDEX_DIR / "chunks.json", "w", encoding="utf-8") as f:
    json.dump(all_chunks, f, indent=2)



print("Documents:", len(documents))
print("Chunks:", len(all_chunks))
print("Vectors:", index.ntotal)
print("Index saved successfully.")

# results = retrieve(
#     "What skills should I learn to become a backend developer?",
#     index,
#     metadata,
#     all_chunks,
#     top_k=3
# )

# print(results)

# print("Vectors stored:",index.ntotal)
# print("chunks:",len(all_chunks))
# print("Embedding shape:",embeddings.shape)


# question = "What skills should I learn to become a backend developer?"
# response = ask_rag(
#  question,
#  index,
#  metadata,
#  all_chunks,
#  top_k=3
# )
# print("QUESTION:")
# print(response["question"])
# print("\nANSWER:")
# print(response["answer"])
# print("\nRETRIEVED CHUNKS:")
# for item in response["retrieved_chunks"]:
#  print("Distance:", item["distance"])
#  print(item["text"][:300])
#  print("-" * 50)