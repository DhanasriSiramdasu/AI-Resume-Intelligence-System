from sentence_transformers import SentenceTransformer

model=SentenceTransformer("all-MiniLM-L6-v2")

def retrieve(query,index,metadata,chunks,top_k=3):
    query_embedding=model.encode([query])

    distances,indices=index.search(
        query_embedding.astype("float32"),
        top_k
    )

    results=[]

    for distance,index_id in zip(
        distances[0],
        indices[0]
    ):

        results.append({
            "text":chunks[index_id],
            "distance":float(distance),
            "metadata":metadata[index_id]
        })
    return results