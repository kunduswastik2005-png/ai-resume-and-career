from pathlib import Path
from dotenv import load_dotenv
from google import genai
import os

load_dotenv(Path(".env"))

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

for model in client.models.list():
    actions = getattr(model, "supported_actions", [])

    if "generateContent" in actions:
        print(model.name, actions)