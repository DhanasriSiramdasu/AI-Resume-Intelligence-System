from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

client=genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

def generate_improvement_recommendations(
    matched_skills,
    missing_skills,
    ats_breakdown  
):
    prompt = build_improvement_prompt(matched_skills, missing_skills, ats_breakdown)
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt)
    return response.text

def build_improvement_prompt(
        matched_skills,
        missing_skills,
        ats_breakdown
):
    return f"""
You are an AI resume improvement assistant.

Matched skills:
{matched_skills}

Missing_skills:
{missing_skills}

ATS breakdown:
{ats_breakdown}

Give practical, truthful resume improvement recommendations.

Rules:
1.Do not invent skills or experience.
2.Do not tell the user to claim a technology they have not used.
3.Seperate resume improvements from skills they should learn.
4.Prioritize high-impact improvemnets.
5.Keep recommendations specific and actionable.
"""


