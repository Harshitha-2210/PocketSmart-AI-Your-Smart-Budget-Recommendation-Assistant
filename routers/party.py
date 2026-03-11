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

class PartyRequest(BaseModel):
    budget: float
    event_type: str
    guests: str
    location: Optional[str] = "Home"
    food_preference: Optional[str] = ""
    includes: Optional[List[str]] = []
    notes: Optional[str] = ""

def get_party_recommendations(budget, event_type, guests, location, food_preference, includes, notes):
    includes_str = ", ".join(includes) if includes else "Catering, Decoration"
    prompt = f"""
You are an expert party and event budget planner for India.

Generate a detailed party budget plan for:
- Total Budget: Rs.{budget}
- Event Type: {event_type}
- Number of Guests: {guests}
- Venue Type: {location}
- Food Preference: {food_preference or 'No preference'}
- Party Needs: {includes_str}
- Special Requests: {notes or 'None'}

Return ONLY a valid JSON object in this exact format (no markdown, no explanation outside JSON):
{{
  "categories": [
    {{
      "name": "Venue",
      "icon": "📍",
      "allocation": 0,
      "items": [
        {{
          "name": "Home venue",
          "description": "Utilizing the home as the venue.",
          "price": 0
        }}
      ]
    }},
    {{
      "name": "Catering",
      "icon": "🍽️",
      "allocation": 15000,
      "items": [
        {{
          "name": "Home-cooked meal",
          "description": "Simple home-cooked meal for {guests} guests.",
          "price": 15000
        }}
      ]
    }}
  ],
  "venues": [
    {{
      "name": "Home",
      "type": "Residential",
      "location": "{location}",
      "cost": 0
    }}
  ],
  "tips": [
    "Book catering at least 2 weeks in advance for better rates",
    "Buy decorations in bulk from wholesale markets for savings"
  ]
}}

Rules:
- Create categories only for the party needs: {includes_str}
- Add a Contingency category (5-10% of budget) for unexpected expenses
- All prices must be realistic for India in 2024-25 in INR
- Sum of all allocations must equal exactly Rs.{budget}
- Venue suggestions should match: {location}
- Return ONLY the JSON, nothing else
"""
    for attempt in range(3):
        try:
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

@router.get("/party-planner")
async def party_planner_page(request: Request):
    return templates.TemplateResponse("party_planner.html", {"request": request})

@router.post("/generate-party")
async def generate_party(data: PartyRequest):
    try:
        recommendations = get_party_recommendations(
            data.budget, data.event_type, data.guests,
            data.location, data.food_preference, data.includes, data.notes
        )
        recommendation_history.append({
            "id": str(uuid.uuid4()),
            "category": "party",
            "budget": data.budget,
            "preferences": {
                "event_type": data.event_type,
                "guests": data.guests,
                "location": data.location,
                "includes": data.includes
            },
            "result": recommendations,
            "timestamp": datetime.utcnow().isoformat()
        })
        return {"recommendations": recommendations, "budget": data.budget}
    except Exception as e:
        return {"detail": f"AI generation failed: {str(e)}"}
