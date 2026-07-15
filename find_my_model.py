import os
from google import genai
from dotenv import load_dotenv

# Load your API key
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    print("Error: API Key not found in .env!")
    exit()

# Initialize the new Unified GenAI Client
client = genai.Client(api_key=API_KEY)

print("🔍 Scanning Google's servers for your authorized models...\n")

try:
    # Query Google for every model your specific key is allowed to touch
    for model in client.models.list():
        print(f"✅ Authorized Model: {model.name}")
except Exception as e:
    print(f"Connection Error: {e}")

print("\nDone! Look for a model containing the word 'flash' in the list above.")