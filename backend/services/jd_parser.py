from services.skill_extractor import extract_detected_skills
from services.skill_taxonony import normalize_skills

def clean_jd(text):
    return text.replace("\n"," ").replace("\r"," ").lower().strip()

jd_text="""Job Title: Backend Python Developer

We are looking for a Backend Python Developer with experience building scalable REST APIs. The candidate should have strong knowledge of Python, FastAPI, SQL databases, Git, Docker, and cloud deployment. Experience with PostgreSQL, MongoDB, JWT Authentication, and CI/CD is preferred.

Required Skills:
- Python
- FastAPI
- REST API
- SQL
- PostgreSQL
- MongoDB
- Git
- Docker

Preferred Skills:
- AWS
- Redis
- Kubernetes"""

jd_text=clean_jd(jd_text)
jd_detected=extract_detected_skills(jd_text)

jd_skills=[]
for category in jd_detected.values():
    jd_skills.extend(category)

jd_normalised_skills=normalize_skills(jd_skills)

def get_jd_normalised_skills():
    return jd_normalised_skills

def get_jd_text():
    return jd_text