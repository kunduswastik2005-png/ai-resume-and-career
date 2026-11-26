from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from backend.app.database.database import engine, Base
from backend.app.models import User, Resume
from backend.app.api.resumes import router as resume_router


app = FastAPI(
    title="AI Resume & Career Guidance API",
    description=(
        "An intelligent career guidance platform "
        "for resume analysis, skill assessment, "
        "and career recommendations."
    ),
    version="1.0.0"
)


# Database initialization
Base.metadata.create_all(bind=engine)


# Register API routes
app.include_router(resume_router)


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "backend"
    }


# Frontend directory
BASE_DIR = Path(__file__).resolve().parents[2]
FRONTEND_DIR = BASE_DIR / "frontend"


# Serve frontend files
app.mount(
    "/",
    StaticFiles(directory=FRONTEND_DIR, html=True),
    name="frontend"
)