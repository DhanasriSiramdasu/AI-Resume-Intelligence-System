from rag.rag_data import index, metadata, all_chunks
from rag.retriever import retrieve
questions = [
 "What should I learn for backend development?",
 "How should I learn FastAPI?",
 "Why is Docker useful?",
 "What are important Git concepts?",
 "When should I learn PostgreSQL?"
]
for question in questions:
 print("\nQUESTION:", question)
 results = retrieve(
 question,
 index,
 metadata,
 all_chunks,
 top_k=3
 )
 for result in results:
    print("SOURCE:", result["metadata"]["source"])
    print("DISTANCE:", result["distance"])
    print("TEXT:", result["text"][:250])
