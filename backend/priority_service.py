"""
JanSakshi AI - Module 4: Explainable Urgency and Priority Intelligence
Computes multi-factor, explainable priority assessments for civic grievances.
Evaluates public safety risk, public health hazard, essential service disruption,
affected population density, complaint duration, repeated report frequency, and photographic evidence.
Strict guardrail: The system provides advisory assessments only; municipal officials retain final statutory authority.
"""

import logging
from typing import Dict, Any, List, Optional

logger = logging.getLogger("JanSakshi.Priority")

# SLA Windows under Andhra Pradesh Public Services Delivery (Citizen's Charter)
SLA_WINDOWS = {
    "Critical": "24 Hours (Emergency Escalation - Rule 4)",
    "High": "48 Hours (Priority Statutory Window)",
    "Medium": "72 Hours (Standard Redressal Timeline)",
    "Low": "7 Days (Routine Maintenance Schedule)"
}


def assess_priority(
    complaint_description: str,
    category: str = "Other",
    vision_severity: Optional[str] = None,
    duplicate_count: int = 0,
    location_str: Optional[str] = None,
    pending_hours: float = 0.0,
    population_density_hint: Optional[str] = None
) -> Dict[str, Any]:
    """
    Module 4 Entrypoint:
    Calculates explainable priority rating (0-100 score and tier: Low/Medium/High/Critical).
    Returns factor-by-factor breakdown, explanation, SLA window, and recommended action.
    """
    desc = (complaint_description or "").lower()
    cat = (category or "Other").title()
    factors = []
    score = 30.0  # Baseline municipal intake score

    # Factor 1: Public Safety Risk (+15 to +35)
    safety_triggers = ["open manhole", "deep pit", "live wire", "electric shock", "sparking",
                       "accident", "collapse", "danger", "hazard", "gas leak", "transformer"]
    critical_safety_found = [t for t in safety_triggers if t in desc]
    if critical_safety_found:
        score += 35.0
        factors.append(f"Immediate Public Safety Risk: High-hazard trigger(s) identified ({', '.join(critical_safety_found[:2])})")
    elif cat in ["Public Safety", "Electricity"]:
        score += 15.0
        factors.append(f"Public Safety Department Classification ({cat})")

    # Factor 2: Public Health & Sanitation Hazard (+15 to +25)
    health_triggers = ["hospital", "school", "drinking water", "contamination", "sewage overflow",
                       "toxic", "stench", "foul smell", "mosquito", "dengue", "epidemic", "nursing home"]
    health_found = [t for t in health_triggers if t in desc]
    if health_found:
        score += 25.0
        factors.append(f"Public Health & Environmental Risk: Proximity or risk factors detected ({', '.join(health_found[:2])})")
    elif cat in ["Drainage", "Water Supply"]:
        score += 15.0
        factors.append("Essential Civic Utility / Drinking Water & Drainage Service")

    # Factor 3: Essential Service Disruption & Arterial Obstruction (+10 to +20)
    disruption_triggers = ["rtc complex", "junction", "bus stand", "railway", "main road", "highway",
                           "traffic jam", "gridlock", "commercial branch", "market", "blocked completely"]
    disruption_found = [t for t in disruption_triggers if t in desc]
    if disruption_found:
        score += 20.0
        factors.append(f"Essential Transit / Economic Disruption: Key civic corridor affected ({', '.join(disruption_found[:2])})")

    # Factor 4: Available Vision Evidence Severity (+10 to +25)
    if vision_severity:
        v_sev = vision_severity.lower()
        if v_sev in ["severe", "critical"]:
            score += 25.0
            factors.append("Photographic Evidence Audit: Visual defect confirmed as Severe by vision inspection")
        elif v_sev == "high":
            score += 18.0
            factors.append("Photographic Evidence Audit: Visual defect confirmed as High severity")
        elif v_sev == "medium":
            score += 8.0
            factors.append("Photographic Evidence Audit: Visual defect confirmed as Moderate severity")

    # Factor 5: Repeated Reports / Citizen Community Volume (+10 to +20)
    if duplicate_count >= 3:
        score += 20.0
        factors.append(f"Community Impact Multiplier: {duplicate_count} corroborating citizen reports received for this cluster")
    elif duplicate_count >= 1:
        score += 10.0
        factors.append(f"Multiple Citizen Reports: Corroborated by {duplicate_count} existing ticket(s) in local area")

    # Factor 6: Elapsed Pending Hours / Latency Escalation (+10 to +20)
    if pending_hours >= 72.0:
        score += 20.0
        factors.append(f"SLA Breach Escalation: Unresolved for {int(pending_hours)} hours exceeding statutory charter window")
    elif pending_hours >= 48.0:
        score += 10.0
        factors.append(f"SLA Warning: Unresolved for {int(pending_hours)} hours")

    # Clamp score between 10.0 and 100.0
    final_score = min(100.0, max(10.0, score))

    # Determine Tier
    if final_score >= 80.0:
        tier = "Critical"
        recommended_action = "Immediate Field Dispatch: Notify Zonal Executive Engineer & dispatch emergency rectification crew within 2 hours."
    elif final_score >= 60.0:
        tier = "High"
        recommended_action = "Expedited Field Audit: Assign Ward Sanitary / Engineering Inspector for on-site inspection within 12 hours."
    elif final_score >= 40.0:
        tier = "Medium"
        recommended_action = "Standard Queue: Schedule for departmental work order allocation under routine ward maintenance roster."
    else:
        tier = "Low"
        recommended_action = "Scheduled Review: Log into weekly zonal infrastructure maintenance plan."

    sla_window = SLA_WINDOWS[tier]

    # Generate Human-Readable Explanation
    if tier == "Critical":
        explanation = (
            f"Evaluated as Critical Priority (Score: {int(final_score)}/100) due to severe safety/health hazards "
            f"or active essential service disruption requiring emergency intervention."
        )
    elif tier == "High":
        explanation = (
            f"Evaluated as High Priority (Score: {int(final_score)}/100) due to substantial civic inconvenience, "
            f"public health contamination risk, or verified photographic severity."
        )
    elif tier == "Medium":
        explanation = (
            f"Evaluated as Medium Priority (Score: {int(final_score)}/100) reflecting routine civic maintenance needs "
            f"with localized impact."
        )
    else:
        explanation = (
            f"Evaluated as Low Priority (Score: {int(final_score)}/100) with minor immediate safety impact."
        )

    return {
        "priority_level": tier,
        "priority_score": round(final_score, 1),
        "explanation": explanation,
        "contributing_factors": factors,
        "recommended_sla": sla_window,
        "recommended_action": recommended_action,
        "official_authority_note": "ADVISORY INTELLIGENCE: Official administrative decisions and statutory certifications remain the sole prerogative of authorized Municipal Officers under the AP Municipal Corporations Act."
    }
