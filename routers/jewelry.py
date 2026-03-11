from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import Optional, List
from google import genai
from dotenv import load_dotenv
from state import recommendation_history
import os, time, uuid
from datetime import datetime

load_dotenv()
router = APIRouter()
templates = Jinja2Templates(directory="templates")
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

class JewelryRequest(BaseModel):
    budget: float
    occasion: str
    jewelry_types: Optional[List[str]] = []
    metal_preference: Optional[str] = ""
    platforms: Optional[List[str]] = ["Amazon", "Flipkart", "Bluestone"]
    style_preferences: Optional[str] = ""
    image: Optional[str] = None  # base64 image

def get_jewelry_recommendations(budget, occasion, jewelry_types, metal_preference, platforms, style_preferences, image_b64):
    types_str    = ", ".join(jewelry_types) if jewelry_types else "Earrings, Necklace, Ring"
    platform_str = ", ".join(platforms)     if platforms     else "Amazon, Flipkart, Bluestone"

    image_note = ""
    if image_b64:
        image_note = "An outfit image has been provided. Analyze the colors, style and formality of the outfit and include that in outfit_analysis."

    prompt = f"""
You are an expert jewelry stylist and budget advisor for India.

Generate personalized jewelry recommendations for:
- Total Budget: Rs.{budget}
- Occasion: {occasion}
- Jewelry Types Wanted: {types_str}
- Metal Preference: {metal_preference or 'No preference'}
- Preferred Platforms: {platform_str}
- Style Preferences: {style_preferences or 'None'}
{image_note}

Return ONLY a valid JSON object in this exact format (no markdown, no extra text):
{{
  "outfit_analysis": {{
    "colors": "blue, white",
    "style": "casual",
    "formality": "informal"
  }},
  "jewelry": [
    {{
      "name": "Pearl Drop Earrings",
      "type": "Earrings",
      "description": "Elegant pearl drop earrings that complement the outfit beautifully.",
      "style": "classic",
      "price": 2500
    }},
    {{
      "name": "Delicate Silver Necklace",
      "type": "Necklace",
      "description": "A simple silver chain with a small pendant, perfect for the occasion.",
      "style": "minimalist",
      "price": 3500
    }}
  ],
  "tips": [
    "Layer delicate pieces for a modern look",
    "Mix metals carefully — stick to one dominant metal",
    "For {occasion}, less is more — choose 2-3 statement pieces"
  ]
}}

Rules:
- Recommend only the jewelry types requested: {types_str}
- All prices must be realistic for India in 2024-25 in INR
- Total of all jewelry prices must not exceed Rs.{budget}
- If no outfit image, set outfit_analysis to null
- Each jewelry item must have name, type, description, style, and price
- Return ONLY the JSON, nothing else
"""

    contents = [prompt]

    if image_b64:
        contents = [
            {
                "role": "user",
                "parts": [
                    {"text": prompt},
                    {"inline_data": {"mime_type": "image/jpeg", "data": image_b64}}
                ]
            }
        ]

    for attempt in range(3):
        try:
            if image_b64:
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=contents
                )
            else:
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt
                )
            return response.text
        except Exception as e:
            if "503" in str(e) and attempt < 2:
                time.sleep(3)
                continue
            raise e

@router.get("/jewelry-planner")
async def jewelry_planner_page(request: Request):
    return templates.TemplateResponse("jewelry_planner.html", {"request": request})

@router.post("/generate-jewelry")
async def generate_jewelry(data: JewelryRequest):
    try:
        recommendations = get_jewelry_recommendations(
            data.budget, data.occasion, data.jewelry_types,
            data.metal_preference, data.platforms,
            data.style_preferences, data.image
        )
        recommendation_history.append({
            "id": str(uuid.uuid4()),
            "category": "jewelry",
            "budget": data.budget,
            "preferences": {
                "occasion": data.occasion,
                "jewelry_types": data.jewelry_types,
                "metal": data.metal_preference,
                "platforms": data.platforms
            },
            "result": recommendations,
            "timestamp": datetime.utcnow().isoformat()
        })
        return {"recommendations": recommendations, "budget": data.budget}
    except Exception as e:
        return {"detail": f"AI generation failed: {str(e)}"}
