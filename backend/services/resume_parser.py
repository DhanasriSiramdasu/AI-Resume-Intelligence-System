SECTION_NAMES={
    "skills":[
        "skills",
        "technical skills",
        "technical skills & tools",
        "technologies",
        "skills & technologies"
    ],
    "education":[
        "education",
        "academic background",
        "educational background"
    ],
    "experience":[
        "experience",
        "professional experience",
        "work experience",
        "employment history"
    ],
    "projects":[
        "projects",
        "personal projects",
        "academic projects"
    ],
    "certifications":[
        "certifications",
        "certificates",
        "licenses & certifications"   
    ],
    "achievements":[
        "achievements",
        "awards",
        "honors"
    ]
}
def detect_section(line: str):
    line = line.lower().strip()
    line = line.rstrip(":").strip()

    for section, names in SECTION_NAMES.items():
        for name in names:
            if line == name.lower():
                return section

    return None

def parse_resume(text:str):
    resume={
        "skills":"",
        "education":"",
        "experience":"",
        "projects":"",
        "certifications":"",
        "achievements":""
    }
    current_section=None
    lines=text.splitlines()
    for line in lines:
        section=detect_section(line)
        if section:
            current_section=section
            continue
        if current_section:
            resume[current_section]+=line.strip()+"\n"
    return resume

def clean_text(text:str):
    lines=text.splitlines()
    cleaned_lines=[]
    for line in lines:
        line=line.strip()
        if line:
            cleaned_lines.append(line)
    return "\n".join(cleaned_lines)

