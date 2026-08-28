SKILL_ALIASES = {
    "react.js": "react",
    "reactjs": "react",
    "react": "react",

    "node": "node.js",
    "nodejs": "node.js",
    "node.js": "node.js",

    "postgres": "postgresql",
    "postgresql": "postgresql",

    "ml": "machine learning",
    "machine learning": "machine learning",

    "natural language processing": "nlp",
    "nlp": "nlp"
}

def normalize_skills(skills):
    normalized=[]
    for skill in skills:
        skill=skill.lower().strip()
        normalized_skill = SKILL_ALIASES.get(
            skill,
            skill
        )

        if normalized_skill not in normalized:
            normalized.append(normalized_skill)

    return normalized