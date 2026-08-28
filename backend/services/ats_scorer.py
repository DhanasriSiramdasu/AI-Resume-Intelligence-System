def calculate_skill_score(resume_skills,jd_skills):
    required=set(skill.lower() for skill in jd_skills)
    matched=set(skill.lower() for skill in resume_skills)
    if not required:
        return 0.0
    found=len(matched.intersection(required))
    return (found/len(required))*100


def calculate_semantic_score(similarity):
    return max(0.0, min(float(similarity) * 100, 100.0))

def calculate_section_score(resume):
    required=[
        "education",
        "experience",
        "skills",
        "projects"
    ]
    detected=0
    for section in required:
        if resume.get(section,"").strip():
            detected+=1
    return round(detected/len(required)*100,2)


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

    if not achievements:
        return 0.0

    text = achievements.lower()

    achievement_types = {
        "award": [
            "award",
            "awarded",
            "winner",
            "won",
            "prize"
        ],

        "rank": [
            "rank",
            "ranked",
            "1st",
            "2nd",
            "3rd",
            "first place",
            "second place",
            "third place"
        ],

        "competition": [
            "contest",
            "competition",
            "hackathon",
            "challenge"
        ],

        "academic": [
            "gate",
            "qualified",
            "cgpa",
            "distinction",
            "scholarship"
        ],

        "coding": [
            "leetcode",
            "geeksforgeeks",
            "solved",
            "coding problems"
        ],

        "quantitative": [
            "%",
            "increased",
            "decreased",
            "improved",
            "reduced",
            "saved"
        ]
    }

    score = 0

    for keywords in achievement_types.values():

        if any(keyword in text for keyword in keywords):
            score += 20

    return min(score, 100.0)

def calculate_experience_score(experience_text, jd_skills):

    if not experience_text.strip():
        return 0.0

    if not jd_skills:
        return 50.0

    text = experience_text.lower()

    matched = 0

    for skill in jd_skills:
        if skill.lower() in text:
            matched += 1

    return round(
        matched / len(jd_skills) * 100,
        2
    )


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
        "experience_relevance":{
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
