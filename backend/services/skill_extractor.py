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

import re

def extract_detected_skills(text:str):
    text=text.lower()
    detected_skills={}
    for category,skills in SKILL_DATABASE.items():
        detected_skills[category]=[]
        for skill in skills:
            escaped_skill=re.escape(skill)
            pattern=r'\b' + escaped_skill + r'\b'
            if re.search(pattern, text):
                detected_skills[category].append(skill)
    return detected_skills