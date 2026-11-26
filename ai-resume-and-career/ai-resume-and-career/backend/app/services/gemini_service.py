import json
from pathlib import Path

from dotenv import load_dotenv
from google import genai


# Load environment variables from project root
BASE_DIR = Path(__file__).resolve().parents[3]
load_dotenv(BASE_DIR / ".env")


def analyze_resume_with_gemini(
    resume_text: str,
    education: str,
    interests: str,
    experience: str
):

    import os

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise RuntimeError("Gemini API key is not configured.")

    client = genai.Client(api_key=api_key)

    prompt = f"""
You are an expert AI resume analyzer and career guidance assistant.

Analyze the candidate's resume and additional information.

RESUME:
{resume_text}

EDUCATION:
{education}

INTERESTS:
{interests}

EXPERIENCE:
{experience}

Return ONLY valid JSON with exactly these fields:

{{
    "profileTitle": "Suggested professional title",
    "summary": "Professional profile summary",
    "resumeSuggestions": [
        "Specific improvement recommendation"
    ],
    "learningResources": [
        "Specific learning recommendation"
    ],
    "careerPaths": [
        {{
            "title": "Career role",
            "reason": "Why this role is relevant",
            "skillsToLearn": "Skills to develop"
        }}
    ]
}}

IMPORTANT RULES:

1. Never invent qualifications, projects, or experience.
2. Use only information supported by the resume.
3. Consider the candidate's stated interests.
4. Make recommendations realistic for their current level.
5. Do not claim that the candidate has skills they have not demonstrated.
6. Return JSON only, without Markdown formatting.
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt,
        config={
            "response_mime_type": "application/json"
        }
    )

    if not response.text:
        raise RuntimeError("Gemini returned an empty response.")

    return json.loads(response.text)