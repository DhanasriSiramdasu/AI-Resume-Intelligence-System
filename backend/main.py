from fastapi import FastAPI
from fastapi import UploadFile
from fastapi import File
from pydantic import BaseModel
import os

# Resume processing
from services.pdf_parser import extract_text_from_pdf
from services.resume_parser import clean_text, parse_resume

# Skills
from services.skill_extractor import (
    extract_detected_skills,
    calculate_skill_coverage,
    get_all_skills,
    calculate_match_score
)

from services.skill_taxonony import normalize_skills

# Semantic matching
from services.semantic_matcher import calculate_cosine_similarity

# Job description
from services.jd_parser import get_jd_text

# ATS scoring
from services.ats_scorer import (
    calculate_skill_score,
    calculate_section_score,
    calculate_semantic_score,
    calculate_project_score,
    calculate_achievement_score,
    calculate_experience_score,
    calculate_ats_score,
    build_ats_breakdown
)

# Recommendations
from services.llm_recommender import generate_llm_recommendations

# RAG
from services.rag_generator import ask_rag

# Saved RAG data
from rag.rag_data import (
    index,
    metadata,
    all_chunks
)


app = FastAPI()


# ============================================================
# RAG QUESTION MODEL
# ============================================================

class QuestionRequest(BaseModel):
    question: str


# ============================================================
# RESUME ANALYSIS ENDPOINT
# ============================================================

@app.post("/upload-resume")
async def upload_resume(
    file: UploadFile = File(...)
):

    # --------------------------------------------------------
    # Validate PDF
    # --------------------------------------------------------

    if not file.filename.lower().endswith(".pdf"):
        return {
            "error": "Only PDF files are allowed"
        }

    # --------------------------------------------------------
    # Save uploaded file temporarily
    # --------------------------------------------------------

    file_path = f"temp_{file.filename}"

    with open(file_path, "wb") as f:

        file_content = await file.read()

        f.write(file_content)

    # --------------------------------------------------------
    # Extract resume text
    # --------------------------------------------------------

    extracted_text = extract_text_from_pdf(file_path)

    cleaned_text = clean_text(extracted_text)

    structured_resume = parse_resume(cleaned_text)

    # --------------------------------------------------------
    # Get Job Description
    # --------------------------------------------------------

    jd_text = get_jd_text()

    # --------------------------------------------------------
    # Semantic similarity
    # --------------------------------------------------------

    cosine_similarity = calculate_cosine_similarity(
        cleaned_text,
        jd_text
    )

    # --------------------------------------------------------
    # Skill extraction
    # --------------------------------------------------------

    resume_detected_skills = extract_detected_skills(
        cleaned_text
    )

    jd_detected_skills = extract_detected_skills(
        jd_text
    )

    # --------------------------------------------------------
    # Get all skills
    # --------------------------------------------------------

    resume_skills = get_all_skills(
        resume_detected_skills
    )

    jd_skills = get_all_skills(
        jd_detected_skills
    )

    # --------------------------------------------------------
    # Normalize skills
    # --------------------------------------------------------

    resume_normalized_skills = normalize_skills(
        resume_skills
    )

    jd_normalized_skills = normalize_skills(
        jd_skills
    )

    # --------------------------------------------------------
    # Skill matching
    # --------------------------------------------------------

    matched, missing, extra, match_score = calculate_match_score(
        resume_normalized_skills,
        jd_normalized_skills
    )

    # --------------------------------------------------------
    # ATS skill score
    # --------------------------------------------------------

    skill_score = calculate_skill_score(
        resume_normalized_skills,
        jd_normalized_skills
    )

    # --------------------------------------------------------
    # Semantic score
    # --------------------------------------------------------

    semantic_score = float(cosine_similarity)

    # --------------------------------------------------------
    # Experience score
    # --------------------------------------------------------

    experience_score = calculate_experience_score(
        structured_resume["experience"],
        jd_normalized_skills
    )

    # --------------------------------------------------------
    # Project score
    # --------------------------------------------------------

    project_score = calculate_project_score(
        structured_resume["projects"]
    )

    # --------------------------------------------------------
    # Section completeness score
    # --------------------------------------------------------

    section_score = calculate_section_score(
        structured_resume
    )

    # --------------------------------------------------------
    # Achievement score
    # --------------------------------------------------------

    achievement_score = calculate_achievement_score(
        structured_resume["achievements"]
    )

    # --------------------------------------------------------
    # ATS breakdown
    # --------------------------------------------------------

    ats_breakdown = build_ats_breakdown(
        skill_score,
        semantic_score,
        experience_score,
        project_score,
        section_score,
        achievement_score
    )

    # --------------------------------------------------------
    # Final ATS score
    # --------------------------------------------------------

    ats_score = calculate_ats_score(
        skill_score,
        semantic_score,
        experience_score,
        project_score,
        section_score,
        achievement_score
    )

    # --------------------------------------------------------
    # LLM recommendations
    # --------------------------------------------------------

    llm_recommendations = generate_llm_recommendations(
        matched,
        missing,
        extra,
        ats_breakdown,
        structured_resume["experience"],
        structured_resume["projects"],
        jd_text
    )

    # --------------------------------------------------------
    # Delete temporary PDF
    # --------------------------------------------------------

    os.remove(file_path)

    # --------------------------------------------------------
    # Return response
    # --------------------------------------------------------

    return {
        "filename": file.filename,

        "resume_detected_skills": resume_detected_skills,

        "jd_detected_skills": jd_detected_skills,

        "skill_coverage": calculate_skill_coverage(
            resume_skills,
            jd_skills
        ),

        "matched_skills": matched,

        "missing_skills": missing,

        "extra_skills": extra,

        "match_score": match_score,

        "cosine_similarity": cosine_similarity,

        "ats_score": ats_score,

        "ats_breakdown": ats_breakdown,

        "llm_recommendations": llm_recommendations
    }


# ============================================================
# CAREER ADVISOR / RAG ENDPOINT
# ============================================================

@app.post("/career-advice")
def career_advice(
    request: QuestionRequest
):

    return ask_rag(
        request.question,
        index,
        metadata,
        all_chunks,
        top_k=3
    )