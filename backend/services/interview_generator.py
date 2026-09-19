from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

client=genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

def build_interview_prompt(
        matched_skills,
        missing_skills
):
    return f"""
You are an expert interviewer. You are tasked with creating a set of interview preparation questions for this candidate.

Matched skills:
{matched_skills}

Missing skills:
{missing_skills}

Generate:
-5 technical questions based on matched skills
-3 practical/scenario questions
-2 questions related to the skill gaps

Do not assume the candidate has experience with a missing skill.
Questions about missing skills should be framed as preparation/learning questions.

Return a clean numbered list.
"""


def generate_interview_questions(
        matched_skills,
        missing_skills
):
    prompt=build_interview_prompt(
        matched_skills,
        missing_skills
    )

    response=client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    return response.text

