
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from pydantic import BaseModel
from typing import Literal

# Load API key from .env
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")


# ---------- AI OUTPUT STRUCTURE ----------

class ComplaintAnalysis(BaseModel):
    detected_language: str
    issue_type: str

    category: Literal[
        "Road Damage",
        "Water Supply",
        "Drainage",
        "Sanitation",
        "Street Lighting",
        "Electricity",
        "Public Safety",
        "Other"
    ]

    structured_description: str
    suggested_department: str

    location_clues: list[str]
    location_needs_confirmation: bool

    priority: Literal["Low", "Medium", "High", "Critical"]
    priority_reason: str

    missing_information: list[str]
    citizen_followup_question: str

    ai_confidence: Literal["Low", "Medium", "High"]


# ---------- GEMINI CLIENT ----------

def get_gemini_client():

    if not API_KEY:
        raise ValueError(
            "GEMINI_API_KEY is missing. Check your .env file."
        )

    return genai.Client(api_key=API_KEY)


# ---------- COMPLAINT UNDERSTANDING ENGINE ----------

def analyze_complaint(description, location=None):

    if not description or not description.strip():
        raise ValueError("Complaint description cannot be empty.")

    client = get_gemini_client()

    prompt = f"""
You are JanSakshi AI, an intelligent civic grievance
understanding assistant.

Your job is to understand citizen complaints written in:
- English
- Telugu
- Telugu written using English letters
- Mixed Telugu and English

Analyze the citizen's complaint carefully.

CITIZEN COMPLAINT:
{description}

CITIZEN-PROVIDED LOCATION:
{location if location else "Not provided"}

INSTRUCTIONS:

1. Understand the actual civic issue.
2. Identify the language used.
3. Classify the complaint into the closest available category.
4. Rewrite it as a clear, structured complaint without changing
   its meaning.
5. Recommend the relevant government department.
6. Extract location clues explicitly mentioned by the citizen.
7. Never invent an exact address, GPS coordinate or landmark.
8. Assess urgency based on public safety, health and service impact.
9. Explain the reason for the priority recommendation.
10. Identify missing information.
11. Ask a useful follow-up question if more information is needed.
12. Estimate confidence in your interpretation.

PRIORITY GUIDANCE:

Low: Minor inconvenience with no apparent immediate risk.
Medium: Routine civic issue affecting a limited area.
High: Significant disruption or possible health/safety concern.
Critical: Immediate threat to life or serious public safety.

Do not automatically assign Critical without clear evidence.

IMPORTANT:
- Recommendations are advisory, not official decisions.
- Do not invent facts.
- Do not assume the complaint is verified.
- Preserve the citizen's original meaning.
- If location is missing, clearly indicate that it needs confirmation.
"""

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=ComplaintAnalysis,
            temperature=0.2
        )
    )

    if response.parsed is not None:
        return response.parsed.model_dump()

    raise ValueError("Gemini returned no structured analysis.")
