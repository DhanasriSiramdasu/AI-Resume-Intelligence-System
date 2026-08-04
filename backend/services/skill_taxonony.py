SKILL_MAP={
    'react':'react','react.js':'react','recatjs':'react',
    'node.js':'node.js','nodejs':'node.js',
    'postgres':'postgresql','postgresql':'postgresql',
    'ml':'machine learning','machine learning':'machine learning',
    'nlp':'natural language processing',
    'natural language processing':'natural language processing'
}
def normalize_skills(skills):
    normalized=[]
    for skill in skills:
        skill=skill.lower().strip()
        normalized.append(SKILL_MAP.get(skill,skill))
    return sorted(list(set(normalized)))