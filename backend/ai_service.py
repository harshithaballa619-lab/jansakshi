"""
JanSakshi AI - Module 1: Intelligent Complaint Understanding
Understands English, Telugu, Telugu in English script (transliteration), and mixed Telugu-English.
Extracts civic defect classification, department, landmarks/location clues, missing data, and urgency.
Strict zero-hallucination guardrail: Never invents exact addresses or GPS coordinates.
"""

import os
import json
import logging
from typing import Literal, Optional, List, Dict, Any
from dotenv import load_dotenv

# Optional pydantic import with safe fallback
try:
    from pydantic import BaseModel, Field
except ImportError:
    BaseModel = object

load_dotenv()

logger = logging.getLogger("JanSakshi.AI")

CATEGORIES = [
    "Road Damage",
    "Water Supply",
    "Drainage",
    "Sanitation",
    "Street Lighting",
    "Electricity",
    "Public Safety",
    "Other"
]

DEPARTMENT_MAP = {
    "Road Damage": "GVMC Roads & Engineering Wing",
    "Water Supply": "GVMC Water Supply & Distribution Wing",
    "Drainage": "GVMC Drainage & Sewage Management",
    "Sanitation": "GVMC Public Health & Sanitation Wing",
    "Street Lighting": "GVMC Electrical & Streetlights Wing",
    "Electricity": "APEPDCL (Discom Coordination Cell)",
    "Public Safety": "Traffic Police & Municipal Enforcement",
    "Other": "General Grievance Redressal Cell"
}


def get_model_name() -> str:
    """Reads GEMINI_MODEL dynamically from env, defaults to gemini-3.8-flash."""
    return os.getenv("GEMINI_MODEL", "gemini-3.8-flash")


def get_api_key() -> Optional[str]:
    return os.getenv("GEMINI_API_KEY")


def fallback_rule_based_understanding(description: str, location: Optional[str] = None) -> Dict[str, Any]:
    """
    Robust rule-based civic complaint parsing fallback when Gemini API
    is unreachable, unconfigured, or rate-limited (429/503/404).
    Recognizes English, Telugu, and Romanized Telugu keywords.
    """
    text = (description or "").lower()
    loc_text = (location or "").strip()

    detected_lang = "English"
    # Check for Telugu unicode range
    if any("\u0c00" <= char <= "\u0c7f" for char in text):
        detected_lang = "Telugu"
    elif any(k in text for k in ["undhi", "undi", "ledu", "chesaru", "cheyandi", "daggara", "roadu", "neeru", "kalava", "chetha"]):
        detected_lang = "Telugu (Transliterated)"
    elif any(k in text for k in ["road", "drain", "water", "garbage", "light"]):
        detected_lang = "English"

    # Category matching
    cat = "Other"
    if any(k in text for k in ["drain", "drainage", "sewage", "sewer", "gutter", "కాలువ", "మురుగు", "దుర్వాసన", "drainu", "kalava"]):
        cat = "Drainage"
    elif any(k in text for k in ["road", "pothole", "gundalu", "asphalt", "cracked", "రోడ్డు", "గుంతలు", "damaged road", "traffic", "roadu"]):
        cat = "Road Damage"
    elif any(k in text for k in ["water", "drinking water", "pipe", "pipeline", "leak", "borewell", "నీరు", "మంచినీరు", "పైపు", "leakage"]):
        cat = "Water Supply"
    elif any(k in text for k in ["garbage", "trash", "waste", "dump", "dustbin", "చెత్త", "డంపింగ్", "chetha"]):
        cat = "Sanitation"
    elif any(k in text for k in ["light", "streetlight", "dark", "pole", "bulb", "స్ట్రీట్ లైట్", "చీకటి", "lightu"]):
        cat = "Street Lighting"
    elif any(k in text for k in ["electric", "current", "wire", "shock", "spark", "ట్రాన్స్‌ఫార్మర్", "విద్యుత్", "transformer"]):
        cat = "Electricity"
    elif any(k in text for k in ["accident", "safety", "danger", "hazard", "threat", "ప్రమాదం", "భద్రత"]):
        cat = "Public Safety"

    dept = DEPARTMENT_MAP.get(cat, "GVMC Grievance Redressal Cell")

    # Location clues
    location_clues = []
    if loc_text:
        location_clues.append(loc_text)
    for token in ["near ", "opposite ", "behind ", "adjacent to ", "junction", "complex", "ward ", "colony", "cross "]:
        if token in text:
            parts = text.split(token)
            if len(parts) > 1:
                clue = token.strip().capitalize() + " " + parts[1].split(".")[0].strip()[:35]
                # Capitalize words nicely
                clue_formatted = " ".join(w.capitalize() for w in clue.split())
                if clue_formatted not in location_clues:
                    location_clues.append(clue_formatted)

    # Location confirmation needed if no specific ward or landmark provided
    has_specific_location = bool(loc_text) or any(
        any(k in c.lower() for k in ["ward", "nagar", "colony", "junction", "complex", "street", "road"])
        for c in location_clues
    ) and len(location_clues) > 0

    # Priority determination
    priority = "Medium"
    priority_reason = "Standard civic defect reported."
    if any(k in text for k in ["danger", "accident", "hospital", "school", "emergency", "electric wire", "sparking", "open manhole"]):
        priority = "Critical"
        priority_reason = "High hazard identified regarding public safety or life-threatening infrastructure."
    elif any(k in text for k in ["overflow", "stench", "health", "flood", "waterlogging", "drinking water", "major"]):
        priority = "High"
        priority_reason = "Significant public health risk or severe disruption of essential civic service."

    missing = []
    if not loc_text and not location_clues:
        missing.append("Specific street name or municipal landmark")
    if len(text.split()) < 6:
        missing.append("More detailed description of defect extent")

    followup = (
        "దయచేసి ఖచ్చితమైన వీధి లేదా సమీప ల్యాండ్‌మార్క్ వివరాలను తెలపండి (Please confirm specific street or landmark)."
        if missing else
        "How long has this condition persisted?"
    )

    return {
        "detected_language": detected_lang,
        "issue_type": f"{cat} Issue",
        "category": cat,
        "structured_description": description.strip(),
        "suggested_department": dept,
        "location_clues": location_clues[:3],
        "location_needs_confirmation": not has_specific_location,
        "priority": priority,
        "priority_reason": f"{priority_reason} (Rule-based assessment)",
        "missing_information": missing,
        "citizen_followup_question": followup,
        "ai_confidence": "Medium",
        "service_status": "fallback_operational"
    }


def analyze_complaint(description: str, location: Optional[str] = None) -> Dict[str, Any]:
    """
    Module 1 Primary Entrypoint.
    Interprets citizen grievances with Gemini API using dynamic model and structured JSON.
    Catches 404, 429, 503, network errors gracefully and applies deterministic fallback.
    """
    if not description or not description.strip():
        raise ValueError("Complaint description cannot be empty.")

    api_key = get_api_key()
    if not api_key:
        logger.warning("GEMINI_API_KEY missing. Applying deterministic fallback analyzer.")
        return fallback_rule_based_understanding(description, location)

    model_name = get_model_name()

    prompt = f"""
You are JanSakshi AI, an intelligent multilingual civic grievance intake engine for Greater Visakhapatnam Municipal Corporation (GVMC).
Analyze the citizen grievance provided below.

The complaint may be in:
- English
- Telugu (తెలుగు)
- Telugu in English script (Transliteration / Tanglish, e.g., 'RTC complex daggara drainage overflow avtundi')
- Mixed Telugu and English

CITIZEN COMPLAINT:
\"\"\"{description}\"\"\"

CITIZEN LOCATION:
\"\"\"{location if location else 'Not explicitly provided'}\"\"\"

ALLOWED CATEGORIES:
{json.dumps(CATEGORIES)}

INSTRUCTIONS:
1. Identify the actual civic issue.
2. Detect language: 'English', 'Telugu', 'Telugu (Transliterated)', or 'Mixed Telugu-English'.
3. Assign EXACTLY ONE category from ALLOWED CATEGORIES.
4. Rewrite into a clean, professional, structured description preserving the citizen's exact factual claims.
5. Recommend the appropriate municipal department (e.g. GVMC Drainage, GVMC Roads, GVMC Public Health, GVMC Electrical).
6. Extract explicit landmark/location clues mentioned by the citizen. NEVER INVENT AN EXACT ADDRESS OR GPS COORDINATES.
7. If location is vague, set location_needs_confirmation to true.
8. Recommend urgency: 'Low', 'Medium', 'High', or 'Critical'. Explain why based on safety and health risks.
9. List missing information if any.
10. Formulate one polite, bilingual follow-up question for the citizen.
11. Provide confidence: 'Low', 'Medium', or 'High'.

Return strictly valid JSON matching this structure:
{{
  "detected_language": "string",
  "issue_type": "string",
  "category": "string",
  "structured_description": "string",
  "suggested_department": "string",
  "location_clues": ["string"],
  "location_needs_confirmation": true/false,
  "priority": "Low|Medium|High|Critical",
  "priority_reason": "string",
  "missing_information": ["string"],
  "citizen_followup_question": "string",
  "ai_confidence": "Low|Medium|High"
}}
"""

    try:
        from google import genai
        from google.genai import types

        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model=model_name,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                temperature=0.1
            )
        )

        if response and response.text:
            text = response.text.strip()
            # Clean possible markdown wrap
            if text.startswith("```json"):
                text = text[7:]
            if text.startswith("```"):
                text = text[3:]
            if text.endswith("```"):
                text = text[:-3]
            parsed = json.loads(text.strip())

            # Validate category
            if parsed.get("category") not in CATEGORIES:
                parsed["category"] = "Other"

            parsed["service_status"] = "gemini_success"
            return parsed

    except Exception as e:
        err_msg = str(e)
        logger.error(f"Gemini API invocation error ({model_name}): {err_msg}")

        # Check for specific HTTP / API error conditions
        status_label = "gemini_error"
        if "429" in err_msg or "ResourceExhausted" in err_msg:
            status_label = "gemini_rate_limited_429"
        elif "503" in err_msg or "Unavailable" in err_msg:
            status_label = "gemini_unavailable_503"
        elif "404" in err_msg or "NotFound" in err_msg:
            status_label = "gemini_model_not_found_404"

        fallback = fallback_rule_based_understanding(description, location)
        fallback["service_status"] = f"{status_label}_fallback_applied"
        fallback["api_note"] = f"Processed with localized semantic rules: {err_msg[:120]}"
        return fallback

    return fallback_rule_based_understanding(description, location)
