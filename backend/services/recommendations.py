def generate_recommendations(
        missing_skills,
        experience_text,
        projects_text
):
    recommendations=[]
    for skill in missing_skills:
        recommendations.append(f"Consider acquiring the skill: {skill}")

    if "fastapi" in experience_text.lower():
        recommendations.append(
            "Highlight your FastAPI experience  because it matches the job."
        )

    if not projects_text.strip():
        recommendations.append(
            "Add relevant projects to strengthen your resume."
        )
    return recommendations