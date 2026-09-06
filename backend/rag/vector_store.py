import faiss
import numpy as np
import json

def create_index(embeddings):
    embeddings=np.array(embeddings).astype("float32")
    dimension=embeddings.shape[1]
    index=faiss.IndexFlatL2(dimension)
    index.add(embeddings)
    return index

def save_index(index,path):
    faiss.write_index(index,str(path))

def load_index(path):
    return faiss.read_index(str(path))


def save_metadata(metadata,path):
    with open(path,"w",encoding="utf-8") as f:
        json.dump(metadata,f,indent=2)


def load_metadata(path):
    with open(path,"r",encoding="utf-8") as f:
        return json.load(f)