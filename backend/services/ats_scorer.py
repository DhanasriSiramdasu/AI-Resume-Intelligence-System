def calculate_skill_score(resume_skills,jd_skills):
    required=set(skill.lower() for skill in jd_skills)
    matched=set(skill.lower() for skill in resume_skills)
    if not required:
        return 0.0
    found=len(matched.intersection(required))
    return (found/len(required))*100


def calculate_semantic_score(similarity):
    return max(0.0, min(float(similarity) * 100, 100.0))

def calculate_section_score(sections):
    required=[
        "education",
        "experience",
        "skills",
        "projects"
    ]
    detected=set(str(s).lower() for s in sections)
    similar=detected.intersection(required)
    return (len(similar)/len(required))*100


def calculate_project_score(projects):
    if not projects.strip():
        return 0.0
    project_lines = [
        line.strip()
        for line in projects.split("\n")
        if line.strip()
    ]
    count = len(project_lines)
    if count >= 2:
        return 100.0
    elif count == 1:
        return 50.0
    return 0.0

def calculate_achievement_score(achievements):
    indicators=[
        "%",
        "increased",
        "decreased",
        "saved",
        "achieved"
    ]
    text=achievements.lower()

    similar=sum(1 for item in indicators if item in text)

    return min(similar*20.0,100.0)

def calculate_experience_score(experience_text,jd_skills):
    if not experience_text:
        return 0.0
    # Implementation for experience score calculation
    text=experience_text.lower()

    same=sum(1 for item in jd_skills if item in text)

    if not jd_skills:
        return 50.0

    return min((same/len(jd_skills)*100),100.0)


def calculate_ats_score(
    skill_score,
    semantic_score,
    experience_score,
    project_score,
    section_score,
    achievement_score
):
    score=(
        skill_score*0.30+
        semantic_score*0.30+
        experience_score*0.15+
        project_score*0.10+
        section_score*0.10+
        achievement_score*0.05
    ) 
    return score


def build_ats_breakdown(
    skill_score,
    semantic_score,
    experience_score,
    project_score,
    section_score,
    achievement_score
):
    return{
        "skill match":{
            "score":round(float(skill_score),2),
            "weight":30
        },
        "semantic_relevance":{
            "score":round(float(semantic_score),2),
            "weight":30
        },
        "experinece_relevance":{
            "score":round(float(experience_score),2),
            "weight":15
        },
        "projects":{
            "score":round(float(project_score),2),
            "weight":10
        },
        "section_completeness":{
            "score":round(float(section_score),2),
            "weight":10
        },
        "achievements":{
            "score":round(float(achievement_score),2),
            "weight":5
        }
    }
