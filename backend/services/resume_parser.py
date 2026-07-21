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
def detect_section(line:str):
    line=line.lower().strip()
    for section,names in SECTION_NAMES.items():
        for name in names:
            if name==line:
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
    lines=text.split("\n")
    for line in lines:
        section=detect_section(line)
        if section:
            current_section=section
        elif current_section:
            resume[current_section]+=line.strip()+"\n"
    return resume

def clean_text(text:str):
    lines=text.split("\n")
    cleaned_lines=[]
    for line in lines:
        if line.strip():
            cleaned_lines.append(line.strip())
    return "\n".join(cleaned_lines)

