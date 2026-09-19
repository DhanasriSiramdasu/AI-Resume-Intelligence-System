from pydantic import BaseModel
from typing import  Any

class AnalysisResponse(BaseModel):
    summary:dict[str,Any]
    skills:dict[str,Any]
    ats_breakdown:dict[str,Any]
    recommendations:Any
    career_advice:Any
    interview_questions:Any