from pathlib import Path
from dotenv import load_dotenv
from google import genai
import os

load_dotenv(Path(".env"))

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Reply with exactly: Gemini connection successful"
)

print(response.text)