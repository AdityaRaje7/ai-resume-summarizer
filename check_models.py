import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load the secret API key
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=API_KEY)

print("🔍 Reaching out to Google Servers....")
print("_" * 40)

# Ask google list of models available
try:
    for m in genai.list_models():
        if 'generatedContent' in m.supported_generated_methods:
            print(f"✅ Model Name: {m.name}")
            print(f"   Model Type: {m.model_type}")
            print(f"   Supported Methods: {m.supported_generated_methods}")
            print(f"   Description: {m.description}")
            print("_" * 40)
except Exception as e:
    print(f"❌ Error while fetching models: {e}")

print("_" * 40)
print("Done! ✅")