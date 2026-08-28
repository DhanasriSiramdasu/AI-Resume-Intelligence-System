from sentence_transformers import SentenceTransformer
model=SentenceTransformer('all-MiniLM-L6-v2')
from sklearn.metrics.pairwise import cosine_similarity

def calculate_cosine_similarity(text1:str,text2:str):
    resume_embedding=get_embedding(text1)
    jd_embedding=get_embedding(text2)
    score=float(cosine_similarity([resume_embedding],[jd_embedding])[0][0])*100
    return score

def get_embedding(text:str):
    return model.encode(text,convert_to_numpy=True)