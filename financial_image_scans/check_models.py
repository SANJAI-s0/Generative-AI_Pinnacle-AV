import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)
    
    print("Available Models for your API Key:\n")
    print("=" * 60)
    
    for model in genai.list_models():
        if 'generateContent' in model.supported_generation_methods:
            print(f"✓ {model.name}")
    print("=" * 60)
else:
    print("Error: GOOGLE_API_KEY not found in .env file")
