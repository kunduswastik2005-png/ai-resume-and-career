import re

SKILL_CATEGORIES = {
    "programming_languages": [
        "python", "java", "javascript", "typescript",
        "c", "c++", "c#", "go", "rust", "php"
    ],
    "web_development": [
        "html", "css", "react", "angular",
        "node.js", "fastapi", "django", "flask"
    ],
    "databases": [
        "mysql", "postgresql", "mongodb",
        "sqlite", "redis", "sql"
    ],
    "data_science_ai": [
        "machine learning", "deep learning",
        "artificial intelligence", "numpy",
        "pandas", "pytorch", "tensorflow",
        "scikit-learn", "data analysis"
    ],
    "tools": [
        "git", "github", "docker", "linux",
        "kubernetes", "vscode", "aws", "azure"
    ],
    "soft_skills": [
        "communication", "leadership",
        "teamwork", "problem solving",
        "critical thinking", "time management"
    ]
}


def extract_skills(text: str) -> dict:
    text = text.lower()
    extracted_skills = {}

    for category, skills in SKILL_CATEGORIES.items():
        found = []

        for skill in skills:
            pattern = r"(?<!\w)" + re.escape(skill.lower()) + r"(?!\w)"

            if re.search(pattern, text):
                found.append(skill)

        extracted_skills[category] = found

    return extracted_skills


def get_all_skills(extracted_skills: dict) -> list:
    """Convert categorized skills into a flat list."""
    return [
        skill
        for skills in extracted_skills.values()
        for skill in skills
    ]