from fastapi import FastAPI
from fastapi import UploadFile
from fastapi import File
import os
from services.pdf_parser import extract_text_from_pdf
from services.resume_parser import clean_text,parse_resume
from services.skill_extractor import extract_detected_skills
from services.skill_taxonony import normalize_skills
from services.jd_parser import get_jd_normalised_skills,get_jd_text
app=FastAPI()

@app.post("/upload-resume")
async def upload_resume(
    file:UploadFile=File(...)
):
    if not file.filename.lower().endswith(".pdf"):
        return {"error": "Only PDF files are allowed"}
    file_path=f"temp_{file.filename}"
    with open(file_path,"wb") as f:
        file_content=await file.read()
        f.write(file_content)
    extracted_text=extract_text_from_pdf(file_path)
    cleaned_text=clean_text(extracted_text)
    structured_resume=parse_resume(cleaned_text)
    resume_detected_skills=extract_detected_skills(cleaned_text)
    jd_detected_skills=extract_detected_skills(get_jd_text())
    skills=get_all_skills(resume_detected_skills)
    resume_normalized_skills=normalize_skills(skills)
    cosine_similarity=float(calculate_cosine_similarity(extracted_text,get_jd_text()))
    os.remove(file_path)
    return{
        "filename":file.filename,
        "raw_text":extracted_text,
        "cleaned_text":cleaned_text,
        "structured_resume":structured_resume,
        "resume_detected_skills": resume_detected_skills,
        "jd_detected_skills": jd_detected_skills,
        "skills":skills,
        "normalized_skills": resume_normalized_skills,
        "skill_coverage": calculate_skill_coverage(
            resume_detected_skills,
            jd_detected_skills
        ),
        "matched,missing,extra,match_score":calculate_match_score(resume_normalized_skills, get_jd_normalised_skills()),
        "cosine_similarity":cosine_similarity
    }

def calculate_skill_coverage(
    resume_detected_skills,
    jd_detected_skills
):
    # Convert both lists to lowercase sets.
    expected = set(
        skill.lower()
        for skill in jd_detected_skills
    )
    detected = set(
        skill.lower()
        for skill in resume_detected_skills
    )
    # Find matching skills.
    matched = expected.intersection(
        detected
    )
    # Avoid division by zero.
    if len(expected) == 0:
        return 0
    # Calculate coverage percentage.
    coverage = (
        len(matched)
        / len(expected)
    ) * 100
    return coverage

def get_all_skills(skills):
    all_skills=[]
    for category in skills.values():
        all_skills.extend(category)
    return all_skills


def calculate_match_score(resume_skills, jd_skills):
    resume_set=set(resume_skills)
    jd_set=set(jd_skills)
    matched=list(resume_set & jd_set)
    missing=list(jd_set - resume_set)
    extra=list(resume_set - jd_set)
    if(len(jd_set)==0):
        return 0
    return matched,missing,extra,round(len(set(resume_skills)& set(jd_skills))/len(jd_skills)*100,2)

def calculate_cosine_similarity(text1,text2):
    from sklearn.metrics.pairwise import cosine_similarity
    score=float(cosine_similarity([get_embedding(text1)],[get_embedding(text2)])[0][0])*100
    return score

from sentence_transformers import SentenceTransformer
model=SentenceTransformer('all-MiniLM-L6-v2')

def get_embedding(text):
    return model.encode(text)

