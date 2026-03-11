from pydantic import BaseModel
from typing import Optional

# ─── Auth Models ───────────────────────────────────────────
class UserBase(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserInDB(UserBase):
    hashed_password: str
    disabled: Optional[bool] = False

class User(UserBase):
    disabled: Optional[bool] = False

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# ─── Planner Models ────────────────────────────────────────
class HomeRequest(BaseModel):
    budget: float
    rooms: list
    style: Optional[str] = "modern"

class PartyRequest(BaseModel):
    budget: float
    guests: int
    event_type: str
    venue: Optional[str] = "indoor"

class JewelryRequest(BaseModel):
    budget: float
    occasion: str
    style: Optional[str] = "elegant"