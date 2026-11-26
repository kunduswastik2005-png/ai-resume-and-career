CAREER_ROLES = {
    "Python Developer": {
        "skills": [
            "python", "sql", "git", "django",
            "flask", "fastapi", "postgresql"
        ]
    },

    "Full Stack Developer": {
        "skills": [
            "html", "css", "javascript", "react",
            "node.js", "sql", "git"
        ]
    },

    "Data Analyst": {
        "skills": [
            "python", "sql", "excel", "pandas",
            "numpy", "data analysis"
        ]
    },

    "Machine Learning Engineer": {
        "skills": [
            "python", "machine learning",
            "deep learning", "numpy", "pandas",
            "pytorch", "scikit-learn"
        ]
    },

    "Backend Developer": {
        "skills": [
            "python", "java", "sql", "postgresql",
            "fastapi", "django", "flask", "git"
        ]
    },

    "DevOps Engineer": {
        "skills": [
            "linux", "docker", "kubernetes",
            "aws", "azure", "git"
        ]
    }
}


def analyze_career_paths(user_skills: list) -> list:
    user_skills = {skill.lower() for skill in user_skills}

    career_paths = []

    for role, details in CAREER_ROLES.items():

        required_skills = details["skills"]

        matched_skills = [
            skill for skill in required_skills
            if skill in user_skills
        ]

        missing_skills = [
            skill for skill in required_skills
            if skill not in user_skills
        ]

        compatibility = round(
            (len(matched_skills) / len(required_skills)) * 100
        )

        career_paths.append({
            "title": role,
            "compatibility": compatibility,
            "matchedSkills": matched_skills,
            "skillsToLearn": missing_skills
        })

    career_paths.sort(
        key=lambda item: item["compatibility"],
        reverse=True
    )

    return career_paths


def calculate_profile_strength(user_skills: list) -> int:
    """
    Estimate profile strength based on the breadth
    of identified technical and professional skills.
    """

    total_skills = len(user_skills)

    score = min(total_skills * 10, 100)

    return score
