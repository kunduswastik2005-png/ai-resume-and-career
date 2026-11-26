from pydantic import BaseModel, Field


class ResumeAnalysisRequest(BaseModel):

    resumeText: str = Field(min_length=40, max_length=30000)

    education: str = ""

    interests: str = ""

    experience: str = ""