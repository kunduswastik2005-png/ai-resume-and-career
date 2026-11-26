from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session

from backend.app.database.database import get_db
from backend.app.models.resume import Resume
from backend.app.services.resume_parser import extract_text
from backend.app.services.skill_extractor import (
    extract_skills,
    get_all_skills
)
from backend.app.schemas.analysis import ResumeAnalysisRequest
from backend.app.services.career_analyzer import (
    analyze_career_paths,
    calculate_profile_strength
)


router = APIRouter(tags=["Resume Management"])


# --------------------------------------------------
# 1. UPLOAD RESUME
# --------------------------------------------------

@router.post("/resumes/upload")
async def upload_resume(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    filename = file.filename or ""
    file_type = "." + filename.rsplit(".", 1)[-1].lower() if "." in filename else ""

    if file_type not in [".pdf", ".docx"]:
        raise HTTPException(
            status_code=400,
            detail="Only PDF and DOCX files are supported."
        )

    content = await file.read()

    if not content:
        raise HTTPException(
            status_code=400,
            detail="Uploaded file is empty."
        )

    if len(content) > 5 * 1024 * 1024:
        raise HTTPException(
            status_code=413,
            detail="File size must not exceed 5 MB."
        )

    try:
        extracted_text = extract_text(content, file_type)

        if not extracted_text:
            raise HTTPException(
                status_code=422,
                detail="No readable text found in the resume."
            )

        resume = Resume(
            file_name=filename,
            file_type=file_type,
            extracted_text=extracted_text
        )

        db.add(resume)
        db.commit()
        db.refresh(resume)

        return {
            "message": "Resume uploaded and processed successfully.",
            "resume_id": resume.id,
            "file_name": resume.file_name,
            "extracted_text": extracted_text
        }

    except HTTPException:
        raise

    except Exception as error:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Resume processing failed: {str(error)}"
        )


# --------------------------------------------------
# 2. ANALYZE STORED RESUME
# --------------------------------------------------

@router.post("/resumes/{resume_id}/analyze")
def analyze_resume(
    resume_id: int,
    db: Session = Depends(get_db)
):
    resume = db.query(Resume).filter(
        Resume.id == resume_id
    ).first()

    if not resume:
        raise HTTPException(
            status_code=404,
            detail="Resume not found."
        )

    skills = extract_skills(resume.extracted_text or "")

    resume.analysis = {
        "skills": skills
    }

    db.commit()
    db.refresh(resume)

    return {
        "message": "Resume analysis completed.",
        "resume_id": resume.id,
        "skills": skills
    }


# --------------------------------------------------
# 3. FRONTEND RESUME ANALYSIS API
# --------------------------------------------------

@router.post("/api/analyze")
def analyze_uploaded_resume(
    payload: ResumeAnalysisRequest,
    db: Session = Depends(get_db)
):
    try:
        # Extract categorized skills
        categorized_skills = extract_skills(payload.resumeText)

        # Convert categorized skills into a flat list
        skills = get_all_skills(categorized_skills)

        if not skills:
            raise HTTPException(
                status_code=422,
                detail="No recognized skills found in the resume."
            )

        # Analyze career compatibility
        career_paths = analyze_career_paths(skills)

        # Calculate profile strength
        profile_strength = calculate_profile_strength(skills)

        # Identify skill gaps
        top_career = career_paths[0]
        skill_gaps = top_career["skillsToLearn"]

        # Resume improvement suggestions
        resume_suggestions = [
            "Add measurable achievements to your resume.",
            "Include detailed descriptions of your projects.",
            "Highlight skills relevant to your target career."
        ]

        # Learning resources
        learning_resources = [
            "Official Python Documentation",
            "freeCodeCamp",
            "Kaggle Learn",
            "GitHub Learning Resources"
        ]

        # Format career recommendations
        formatted_careers = []

        for career in career_paths[:5]:
            formatted_careers.append({
                "title": career["title"],
                "reason": (
                    f"You match {career['compatibility']}% "
                    "of the identified skills for this role."
                ),
                "skillsToLearn": ", ".join(
                    career["skillsToLearn"][:5]
                )
            })

        # Prepare frontend-compatible response
        result = {
            "profileTitle": top_career["title"],
            "summary": (
                f"Your resume contains {len(skills)} recognized skills. "
                f"Your strongest current career match is "
                f"{top_career['title']}."
            ),
            "profileStrength": profile_strength,
            "skills": skills,
            "skillGaps": skill_gaps,
            "careerPaths": formatted_careers,
            "learningResources": learning_resources,
            "resumeSuggestions": resume_suggestions
        }

        # Save analysis in PostgreSQL
        resume = Resume(
            file_name="browser-upload.txt",
            file_type=".txt",
            extracted_text=payload.resumeText,
            analysis=result
        )

        db.add(resume)
        db.commit()
        db.refresh(resume)

        result["resumeId"] = resume.id

        return result

    except HTTPException:
        raise

    except Exception as error:
        db.rollback()

        raise HTTPException(
            status_code=500,
            detail=f"Resume analysis failed: {str(error)}"
        )