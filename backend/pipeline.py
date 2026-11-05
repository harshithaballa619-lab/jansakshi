"""
JanSakshi AI - Coordinated AI Processing Pipeline Orchestrator
Coordinates all six AI intelligence services into a unified, fault-tolerant execution graph.
If any individual service encounters a network timeout or failure, the remaining services
continue and return partial structured results with transparent per-module status reporting.
"""

import os
import json
import logging
import uuid
from typing import Dict, Any, Optional, List
from datetime import datetime

try:
    from .database import get_db_connection
    from .ai_service import analyze_complaint
    from .vision_service import analyze_photo
    from .authenticity_service import screen_evidence_authenticity
    from .duplicate_service import detect_duplicates
    from .priority_service import assess_priority
    from .prediction_service import generate_predictive_insights
except (ImportError, ValueError):
    from database import get_db_connection
    from ai_service import analyze_complaint
    from vision_service import analyze_photo
    from authenticity_service import screen_evidence_authenticity
    from duplicate_service import detect_duplicates
    from priority_service import assess_priority
    from prediction_service import generate_predictive_insights

logger = logging.getLogger("JanSakshi.Pipeline")


def run_complete_pipeline(
    description: str,
    location: Optional[str] = None,
    latitude: Optional[float] = None,
    longitude: Optional[float] = None,
    image_bytes: Optional[bytes] = None,
    image_mime: str = "image/jpeg",
    save_to_db: bool = True
) -> Dict[str, Any]:
    """
    Executes the 6-module coordinated pipeline:
      Step 1: Intelligent Multilingual Complaint Understanding
      Step 2: AI Photo & Civic Defect Vision Analysis (if image provided)
      Step 3: AI Evidence Authenticity & Deepfake Screening (if image provided)
      Step 4: AI Duplicate Detection against prior records
      Step 5: Explainable Urgency & Priority Intelligence
      Step 6: Database Persistence & Token Allocation
      Step 7: Real-time Predictive Insights snapshot
    """
    execution_start = datetime.now()
    module_statuses = {}
    complaint_id = "JS-VSKP" + uuid.uuid4().hex[:6].upper()

    # ----------------------------------------------------
    # STEP 1: Intelligent Complaint Understanding
    # ----------------------------------------------------
    try:
        understanding = analyze_complaint(description, location)
        module_statuses["module_1_complaint_understanding"] = understanding.get("service_status", "operational")
    except Exception as e:
        logger.error(f"Module 1 failure: {e}")
        understanding = {
            "error": str(e),
            "category": "Other",
            "priority": "Medium",
            "suggested_department": "GVMC General Redressal Cell",
            "structured_description": description,
            "detected_language": "Unknown"
        }
        module_statuses["module_1_complaint_understanding"] = "failed"

    category = understanding.get("category", "Other")

    # ----------------------------------------------------
    # STEP 2 & 3: Vision Analysis & Authenticity Screening
    # ----------------------------------------------------
    if image_bytes and len(image_bytes) > 0:
        # Step 2: Vision Defect Analysis
        try:
            vision_result = analyze_photo(
                image_bytes=image_bytes,
                mime_type=image_mime,
                complaint_description=description
            )
            module_statuses["module_2_photo_analysis"] = vision_result.get("service_status", "operational")
        except Exception as e:
            logger.error(f"Module 2 failure: {e}")
            vision_result = {
                "error": str(e),
                "detected_issue": "Unverified Visual Defect",
                "visible_severity": "Medium",
                "confidence": 0.0
            }
            module_statuses["module_2_photo_analysis"] = "failed"

        # Step 3: Evidence Authenticity Screening
        try:
            authenticity_result = screen_evidence_authenticity(
                image_bytes=image_bytes,
                complaint_description=description,
                claimed_category=category,
                mime_type=image_mime
            )
            module_statuses["module_6_authenticity_screening"] = "operational"
        except Exception as e:
            logger.error(f"Module 6 failure: {e}")
            authenticity_result = {
                "error": str(e),
                "evidence_risk_level": "Verification inconclusive",
                "recommended_human_review": True
            }
            module_statuses["module_6_authenticity_screening"] = "failed"
    else:
        vision_result = {
            "detected_issue": "No photographic evidence provided",
            "visible_severity": "None",
            "confidence": 0.0,
            "evidence_limitations": "Citizen did not attach a photograph."
        }
        authenticity_result = {
            "evidence_risk_level": "No photograph supplied",
            "recommended_human_review": False,
            "notes": "Text-only grievance registered."
        }
        module_statuses["module_2_photo_analysis"] = "skipped_no_photo"
        module_statuses["module_6_authenticity_screening"] = "skipped_no_photo"

    # ----------------------------------------------------
    # STEP 4: AI Duplicate Detection
    # ----------------------------------------------------
    try:
        conn = get_db_connection()
        rows = conn.execute("SELECT * FROM complaints ORDER BY created_at DESC LIMIT 50").fetchall()
        existing_complaints = [dict(r) for r in rows]
        conn.close()

        duplicates_result = detect_duplicates(
            new_description=description,
            new_category=category,
            new_lat=latitude,
            new_lon=longitude,
            existing_complaints=existing_complaints
        )
        module_statuses["module_3_duplicate_detection"] = duplicates_result.get("service_status", "operational")
    except Exception as e:
        logger.error(f"Module 3 failure: {e}")
        duplicates_result = {
            "is_likely_duplicate": False,
            "highest_similarity_score": 0.0,
            "error": str(e)
        }
        module_statuses["module_3_duplicate_detection"] = "failed"

    # ----------------------------------------------------
    # STEP 5: Explainable Urgency & Priority Intelligence
    # ----------------------------------------------------
    try:
        dup_count = len(duplicates_result.get("matched_complaints", []))
        vis_sev = vision_result.get("visible_severity")
        priority_result = assess_priority(
            complaint_description=description,
            category=category,
            vision_severity=vis_sev if vis_sev != "None" else None,
            duplicate_count=dup_count,
            location_str=location
        )
        module_statuses["module_4_priority_intelligence"] = "operational"
    except Exception as e:
        logger.error(f"Module 4 failure: {e}")
        priority_result = {
            "priority_level": understanding.get("priority", "Medium"),
            "priority_score": 50.0,
            "recommended_sla": "48 Hours",
            "explanation": "Standard priority applied.",
            "error": str(e)
        }
        module_statuses["module_4_priority_intelligence"] = "failed"

    # ----------------------------------------------------
    # STEP 6: Safe Database Persistence
    # ----------------------------------------------------
    created_at = datetime.now().isoformat(timespec="seconds")
    if save_to_db:
        try:
            conn = get_db_connection()
            conn.execute("""
                INSERT INTO complaints (
                    id, description, category, location, latitude, longitude,
                    image_path, ai_summary, ai_priority, status, created_at,
                    department, detected_language, location_clues, missing_information,
                    followup_question, vision_detected_issue, vision_description,
                    vision_severity, vision_clarity, vision_confidence,
                    duplicate_cluster_id, is_duplicate, duplicate_match_id,
                    duplicate_similarity, duplicate_reason, priority_score,
                    priority_reason, priority_factors, recommended_action,
                    recommended_sla, authenticity_status, provenance_status,
                    watermark_status, metadata_status, manipulation_indicators,
                    synthetic_risk_level, authenticity_confidence,
                    human_review_required, raw_ai_analysis
                ) VALUES (
                    ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                    ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                    ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                    ?, ?, ?, ?, ?, ?, ?, ?, ?
                )
            """, (
                complaint_id,
                description,
                category,
                location or (understanding.get("location_clues", [""])[0] if understanding.get("location_clues") else None),
                latitude,
                longitude,
                None,  # image path placeholder or saved filename
                understanding.get("structured_description"),
                priority_result.get("priority_level"),
                "Submitted",
                created_at,
                understanding.get("suggested_department"),
                understanding.get("detected_language"),
                json.dumps(understanding.get("location_clues", [])),
                json.dumps(understanding.get("missing_information", [])),
                understanding.get("citizen_followup_question"),
                vision_result.get("detected_issue"),
                vision_result.get("visual_description"),
                vision_result.get("visible_severity"),
                vision_result.get("image_clarity"),
                vision_result.get("confidence"),
                duplicates_result.get("duplicate_cluster_id"),
                1 if duplicates_result.get("is_likely_duplicate") else 0,
                duplicates_result.get("matching_complaint_id"),
                duplicates_result.get("highest_similarity_score"),
                duplicates_result.get("explanation"),
                priority_result.get("priority_score"),
                priority_result.get("explanation"),
                json.dumps(priority_result.get("contributing_factors", [])),
                priority_result.get("recommended_action"),
                priority_result.get("recommended_sla"),
                authenticity_result.get("evidence_risk_level"),
                authenticity_result.get("provenance_status"),
                authenticity_result.get("watermark_status"),
                authenticity_result.get("metadata_status"),
                json.dumps(authenticity_result.get("manipulation_indicators", [])),
                authenticity_result.get("evidence_risk_level"),
                authenticity_result.get("confidence"),
                1 if authenticity_result.get("recommended_human_review") else 0,
                json.dumps({
                    "understanding": understanding,
                    "vision": vision_result,
                    "authenticity": authenticity_result,
                    "duplicates": duplicates_result,
                    "priority": priority_result
                })
            ))
            conn.commit()
            conn.close()
            module_statuses["database_persistence"] = "saved_success"
        except Exception as e:
            logger.error(f"Database save error: {e}")
            module_statuses["database_persistence"] = f"save_error: {str(e)[:100]}"

    # ----------------------------------------------------
    # STEP 7: Module 5 Analytics Update
    # ----------------------------------------------------
    try:
        conn = get_db_connection()
        all_rows = conn.execute("SELECT * FROM complaints").fetchall()
        all_records = [dict(r) for r in all_rows]
        conn.close()
        predictive_insights = generate_predictive_insights(all_records)
        module_statuses["module_5_predictive_analytics"] = "operational"
    except Exception as e:
        logger.error(f"Module 5 analytics generation error: {e}")
        predictive_insights = {"error": str(e)}
        module_statuses["module_5_predictive_analytics"] = "failed"

    elapsed_ms = (datetime.now() - execution_start).total_seconds() * 1000

    return {
        "status": "success",
        "complaint_id": complaint_id,
        "created_at": created_at,
        "processing_time_ms": round(elapsed_ms, 1),
        "module_statuses": module_statuses,
        "triage_summary": {
            "category": category,
            "department": understanding.get("suggested_department"),
            "priority": priority_result.get("priority_level"),
            "sla": priority_result.get("recommended_sla"),
            "officer_assigned": "Sri K. V. Ramanamurthy (Executive Officer)",
            "action_plan": priority_result.get("recommended_action")
        },
        "modules": {
            "module_1_understanding": understanding,
            "module_2_vision": vision_result,
            "module_3_duplicates": duplicates_result,
            "module_4_priority": priority_result,
            "module_5_predictive": predictive_insights,
            "module_6_authenticity": authenticity_result
        }
    }
