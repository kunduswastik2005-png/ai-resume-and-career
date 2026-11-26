from pathlib import Path
from dotenv import load_dotenv
from google import genai
import os

load_dotenv(Path(".env"))

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

response = client.interactions.create(
    model="gemini-3.8-flash",
    input="Reply with exactly: Gemini connection successful"
)

print(response)