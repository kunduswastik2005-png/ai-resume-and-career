AI RESUME & CAREER GUIDANCE
# AI Resume & Career Guidance Platform

An intelligent resume analysis and career guidance platform designed to help students and job seekers understand their skills, evaluate their career readiness, identify skill gaps, and discover suitable career opportunities.

The platform analyzes uploaded resumes and generates personalized career recommendations based on the skills and information extracted from them.

## Features

### 1. Resume Analysis
- Upload resumes in PDF, DOCX, and TXT formats.
- Extract resume content automatically.
- Analyze extracted information using Python-based processing.
- Generate a structured resume analysis report.

### 2. Skill Extraction
- Automatically identify technical and soft skills.
- Categorize recognized skills into different domains:
  - Programming Languages
  - Web Development
  - Databases
  - Data Science and AI
  - Development Tools
  - Soft Skills

### 3. Career Recommendations
- Identify suitable career paths based on extracted skills.
- Calculate skill-matching percentages.
- Display missing skills for different career roles.
- Recommend skills to learn for career development.

### 4. Resume Strength Assessment
- Generate a prototype profile-strength score.
- Display recognized skills.
- Provide suggestions to improve resume quality.

### 5. Learning Resources
Recommend learning resources to help users develop missing skills and improve their career readiness.

## Technology Stack

| Component | Technology |
|---|---|
| Frontend | HTML, CSS, JavaScript |
| Backend | Python, FastAPI |
| Database | PostgreSQL |
| ORM | SQLAlchemy |
| Data Validation | Pydantic |
| PDF Processing | PyMuPDF |
| DOCX Processing | python-docx |
| API Documentation | Swagger UI |
| Frontend PDF Extraction | PDF.js |
| Frontend DOCX Extraction | Mammoth.js |

## Project Architecture

```text
ai-resume-and-career/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── resumes.py
│   │   │
│   │   ├── core/
│   │   │
│   │   ├── database/
│   │   │   └── database.py
│   │   │
│   │   ├── models/
│   │   │   ├── user.py
│   │   │   └── resume.py
│   │   │
│   │   ├── schemas/
│   │   │   └── analysis.py
│   │   │
│   │   ├── services/
│   │   │   ├── resume_parser.py
│   │   │   ├── skill_extractor.py
│   │   │   ├── career_analyzer.py
│   │   │   └── gemini_service.py
│   │   │
│   │   └── main.py
│   │
│   └── requirements.txt
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── app.js
│
├── .env
├── .gitignore
└── README.md
```

## Installation and Setup

Follow these steps to run the project locally.

### Prerequisites

Make sure you have installed:

- Python 3.11 or later
- PostgreSQL
- Git
- A modern web browser

### 1. Clone the Repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
```

Navigate into the project directory:

```bash
cd ai-resume-and-career
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```bash
pip install -r backend/requirements.txt
```

### 4. Configure PostgreSQL

Create a PostgreSQL database:

```sql
CREATE DATABASE ai_resume_db;
```

The application uses PostgreSQL to store resume records.

### 5. Configure Environment Variables

Create a `.env` file in the project root.

Add your database configuration:

```env
DATABASE_URL=postgresql+psycopg://postgres:YOUR_PASSWORD@localhost:5433/ai_resume_db
GEMINI_API_KEY=
```

Replace `YOUR_PASSWORD` with your PostgreSQL password.

**Security Notice:** Never upload your `.env` file or expose API credentials on GitHub.

### 6. Run the Application

Start the FastAPI development server:

```bash
uvicorn backend.app.main:app --reload
```

The application will be available at:

**Frontend:**
http://127.0.0.1:8000/

**API Documentation:**
http://127.0.0.1:8000/docs

**Backend Health Check:**
http://127.0.0.1:8000/health

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/analyze` | Analyze uploaded resume text |
| POST | `/resumes/upload` | Upload and store a resume |
| POST | `/resumes/{resume_id}/analyze` | Analyze an existing resume |
| GET | `/health` | Check backend health |

Interactive API documentation is available through Swagger UI at `/docs`.

## How It Works

The platform follows this workflow:

1. The user uploads a resume.
2. The frontend extracts readable text from the selected document.
3. The extracted text is sent to the FastAPI backend.
4. The backend processes the resume.
5. The skill extraction service identifies recognized skills.
6. The career analyzer compares extracted skills against predefined career profiles.
7. The platform identifies skill gaps and calculates career-matching percentages.
8. The analysis is stored in PostgreSQL.
9. The frontend displays the generated career guidance report.

## Current Analysis Approach

The current prototype uses deterministic Python-based analysis.

- Skill extraction uses predefined skill categories.
- Career matching uses predefined skill requirements for different job roles.
- Profile strength is calculated using a prototype skill-count-based scoring method.
- Career recommendations are generated through rule-based matching.

The current profile-strength score is an indicative prototype metric, not a validated measure of employability.

## Future Enhancements

Potential improvements include:

- Context-aware AI-powered resume analysis.
- Advanced NLP-based skill extraction.
- More comprehensive career recommendations.
- Job-market trend analysis.
- Personalized learning roadmaps.
- Resume improvement suggestions using generative AI.
- User authentication and personalized dashboards.
- Expanded career and skill databases.

## Security and Privacy

- Database credentials and API keys should remain in environment variables.
- The `.env` file must not be committed to version control.
- Resume content is stored in the configured PostgreSQL database.
- Do not upload real personal resumes to publicly accessible deployments without appropriate privacy and security controls.

## Project Status

**Status:** Working Prototype

The core resume analysis workflow, skill extraction, career matching, PostgreSQL persistence, and frontend-backend integration have been implemented and tested locally.

## Author

Developed as an academic project focused on applying Python, backend development, database management, and intelligent career guidance techniques.

---

*AI Resume & Career Guidance — Turning resume information into actionable career insights.*
