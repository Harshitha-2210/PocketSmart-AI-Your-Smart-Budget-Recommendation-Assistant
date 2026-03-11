from google import genai
from google.genai import types
from dotenv import load_dotenv
from PIL import Image
import os

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

# ✅ Test 1: Text-only
print("--- Text Test ---")
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Say hello and introduce yourself briefly."
)
print(response.text)

# ✅ Test 2: Image + Text
print("\n--- Multimodal Test ---")
image = Image.open("test_image.jpg")
response2 = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=["What do you see in this image? Describe it briefly.", image]
)
print(response2.text)