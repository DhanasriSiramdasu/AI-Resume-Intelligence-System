import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client=genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

def generate_llm_recommendations(
    matched_skills,
    missing_skills,
    extra_skills,
    ats_breakdown,
    experience,
    projects,
    job_description
):
    prompt=f"""
You are an expert resume optimization assistant.
Analyse the candidate's resume information against the job description.
JOB_DESCRIPTION:
{job_description}

MATCHED SKILLS:
{matched_skills}

MISSING SKILLS:
{missing_skills}

EXTRA SKILLS:
{extra_skills}

ATS BREAKDOWN:
{ats_breakdown}

EXPERIENCE:
{experience}

PROJECTS:
{projects}

Give practical ,job_specific recommendations.

Rules:
1.Never invent skills, experience, projects or achievements. 
2.Recommend a missing skill only if the candidate actually has relevant experience. 
3.Identify which existing experience should be emphasized. 
4.identify which projects are relevant to the job. 
5.Suggest resume improvements that are truthful. 
6.Keep recommendations concise. 

Return JSON with:
summary,
missing_skill_recommendations
experience_recommendations
project_recommendations
resume_improvements
"""

    response=client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text