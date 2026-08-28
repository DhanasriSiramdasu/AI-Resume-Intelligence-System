import re
SKILL_DATABASE = {
    "programming_languages": [
        "python",
        "java",
        "javascript",
        "c",
        "c++"
    ],
    "web": [
        "html",
        "css",
        "react",
        "node.js",
        "fastapi",
        "flask"
    ],
    "databases": [
        "mysql",
        "postgresql",
        "mongodb",
        "sqlite"
    ],
    "machine_learning": [
        "machine learning",
        "deep learning",
        "nlp",
        "natural language processing",
        "computer vision",
        "xgboost"
    ],
    "tools": [
        "git",
        "github",
        "docker"
    ]
}

def extract_detected_skills(text: str):

    detected_skills = {}

    for category, skills in SKILL_DATABASE.items():

        detected_skills[category] = []

        for skill in skills:

            if skill_exists(text, skill):
                detected_skills[category].append(skill)

    return detected_skills


def skill_exists(text: str, skill: str) -> bool:

    pattern = r"(?<!\w)" + re.escape(skill.lower()) + r"(?!\w)"

    return re.search(pattern, text.lower()) is not None


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

