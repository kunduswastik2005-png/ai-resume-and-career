from backend.app.services.gemini_service import analyze_resume_with_gemini


sample_resume = """
John Doe

Education:
B.Tech Computer Science

Skills:
Python, Java, SQL, HTML, CSS

Projects:
Student Management System using Python and MySQL.

Experience:
Fresher
"""

result = analyze_resume_with_gemini(
    resume_text=sample_resume,
    education="B.Tech Computer Science",
    interests="Backend Development and Artificial Intelligence",
    experience="Fresher"
)

print(result)