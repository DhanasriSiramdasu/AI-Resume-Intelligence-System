from fastapi import FastAPI
from fastapi import UploadFile
from fastapi import File
import os
from services.pdf_parser import extract_text_from_pdf
from services.resume_parser import clean_text,parse_resume
from services.skill_extractor import extract_detected_skills,calculate_skill_coverage,get_all_skills,calculate_match_score
from services.skill_taxonony import normalize_skills
from services.semantic_matcher import calculate_cosine_similarity
from services.jd_parser import get_jd_text
from services.ats_scorer import calculate_skill_score,calculate_section_score,calculate_semantic_score,calculate_project_score,calculate_achievement_score,calculate_experience_score,calculate_ats_score,build_ats_breakdown
from services.recommendations import generate_recommendations
from services.llm_recommender import generate_llm_recommendations

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
    cosine_similarity=calculate_cosine_similarity(cleaned_text,get_jd_text())
    resume_detected_skills = extract_detected_skills(cleaned_text)
    jd_detected_skills = extract_detected_skills(get_jd_text())

    resume_skills = get_all_skills(resume_detected_skills)
    jd_skills = get_all_skills(jd_detected_skills)

    resume_normalized_skills = normalize_skills(resume_skills)
    jd_normalized_skills = normalize_skills(jd_skills)
    matched, missing, extra, match_score = calculate_match_score(
    resume_normalized_skills,
    jd_normalized_skills)
    skill_score = calculate_skill_score(
        resume_normalized_skills,
        jd_normalized_skills
    )

    semantic_score = float(cosine_similarity)

    experience_score = calculate_experience_score(
        structured_resume["experience"],
        jd_normalized_skills
    )

    project_score = calculate_project_score(
        structured_resume["projects"]
    )

    section_score = calculate_section_score(
        structured_resume
    )

    achievement_score = calculate_achievement_score(
        structured_resume["achievements"]
    )

    ats_breakdown=build_ats_breakdown(
        skill_score,
        semantic_score,
        experience_score,
        project_score,
        section_score,
        achievement_score
    )

    os.remove(file_path)
    return{
        "filename":file.filename,
        # "structured_resume":structured_resume,
        "resume_detected_skills": resume_detected_skills,
        "jd_detected_skills": jd_detected_skills,
        "skill_coverage": calculate_skill_coverage(
            get_all_skills(resume_detected_skills),
            get_all_skills(jd_detected_skills)
        ),
        "matched_skills": matched,
        "missing_skills": missing,
        "extra_skills": extra,
        "match_score": match_score,
        "cosine_similarity":cosine_similarity,
        "ats_score":calculate_ats_score(
            skill_score,
            semantic_score,
            experience_score,
            project_score,
            section_score,
            achievement_score
        ),
        "ats_breakdown": ats_breakdown,
        "llm_recommendations":generate_llm_recommendations(
            matched,
            missing,
            extra,
            ats_breakdown,
            structured_resume["experience"],
            structured_resume["projects"],
            get_jd_text()
        )
    }






