from pathlib import Path
from xml.parsers.expat import model
from retriever import retrieve
from vector_store import create_index

DOCUMENT_DIR= Path(__file__).parent/"documents"

documents=[]

for file in DOCUMENT_DIR.glob("*.txt"):
    text=file.read_text(encoding="utf-8").strip()

    if text:
        documents.append({
            "source":file.name,
            "text":text
        })

print("Documents ingested:",len(documents))

for document in documents:
    print(document["source"])


def chunk_text(text,chunk_size=500,overlap=50):
    chunks=[]
    start=0

    while start<len(text):
        end=start+chunk_size
        chunks.append(text[start:end])
        start+=chunk_size-overlap
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
            "source":document["source"],
            "text":chunk
        })

from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

embeddings=model.encode(all_chunks)

index=create_index(embeddings)

results = retrieve(
    "What skills should I learn to become a backend developer?",
    index,
    all_chunks,
    top_k=3
)

print(results)

print("Vectors stored:",index.ntotal)
print("chunks:",len(all_chunks))
print("Embedding shape:",embeddings.shape)