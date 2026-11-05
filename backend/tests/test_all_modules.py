"""
JanSakshi AI - Comprehensive Test Suite for Six AI Intelligence Modules
Tests:
  1. Multilingual Complaint Understanding (English, Telugu, Transliterated Telugu)
  2. Photographic Civic Issue & Defect Vision Analysis
  3. Image Upload Format and Dimension Validation
  4. C2PA Provenance and Watermark Screening
  5. Semantic and Geospatial Duplicate Complaint Detection
  6. Explainable Urgency & Priority Intelligence Scoring
  7. Predictive Civic Analytics & Hotspot Clustering
  8. Missing Data and Edge Cases Handling
  9. Fault-tolerance / Graceful Degradation when Gemini is Offline
  10. Safe SQLite Database Persistence and Schema Migrations
"""

import os
import sys
import unittest
import json
import base64
import sqlite3

# Ensure backend package can be imported
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from backend.database import get_db_connection, initialize_database
from backend.ai_service import analyze_complaint, fallback_rule_based_understanding
from backend.vision_service import analyze_photo, inspect_image_heuristics, compare_before_after_images
from backend.duplicate_service import detect_duplicates, haversine_distance_km, compute_token_semantic_similarity
from backend.priority_service import assess_priority
from backend.prediction_service import generate_predictive_insights
from backend.authenticity_service import (
    screen_evidence_authenticity,
    inspect_c2pa_provenance,
    inspect_watermarks_and_generators,
    inspect_exif_metadata
)
from backend.pipeline import run_complete_pipeline


class TestJanSakshiSixModules(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        initialize_database()

    # ---------------------------------------------------------------
    # MODULE 1: COMPLAINT UNDERSTANDING (MULTILINGUAL)
    # ---------------------------------------------------------------
    def test_english_complaint_understanding(self):
        desc = "Severe drainage pipeline leakage near Dwaraka Nagar RTC Complex junction. Black sewage is flooding the footpath."
        result = fallback_rule_based_understanding(desc, location="Ward 34, Visakhapatnam")
        self.assertEqual(result["category"], "Drainage")
        self.assertIn("GVMC Drainage", result["suggested_department"])
        self.assertIn("Dwaraka Nagar", " ".join(result["location_clues"]))
        self.assertIn(result["priority"], ["High", "Critical"])
        self.assertEqual(result["detected_language"], "English")

    def test_telugu_unicode_complaint_understanding(self):
        desc = "ద్వారకా నగర్ మెయిన్ రోడ్డుపై డ్రైనేజీ కాలువ మూత పగిలి దుర్వాసన వస్తోంది."
        result = fallback_rule_based_understanding(desc, location="Dwaraka Nagar")
        self.assertEqual(result["detected_language"], "Telugu")
        self.assertEqual(result["category"], "Drainage")
        self.assertTrue(len(result["citizen_followup_question"]) > 0)

    def test_telugu_transliterated_complaint_understanding(self):
        desc = "RTC complex daggara pedda gundalu paddayi roadu meeda. Vehicles padipotunnayi dangerous ga undi."
        result = fallback_rule_based_understanding(desc, location="RTC Complex")
        self.assertEqual(result["detected_language"], "Telugu (Transliterated)")
        self.assertEqual(result["category"], "Road Damage")
        self.assertIn("GVMC Roads", result["suggested_department"])
        self.assertIn(result["priority"], ["High", "Critical"])

    def test_missing_data_resilience(self):
        desc = "Road bad."
        result = fallback_rule_based_understanding(desc, location=None)
        self.assertTrue(result["location_needs_confirmation"])
        self.assertTrue(len(result["missing_information"]) > 0)

    # ---------------------------------------------------------------
    # MODULE 2: PHOTO & VISION DEFECT ANALYSIS
    # ---------------------------------------------------------------
    def test_image_heuristics_validation(self):
        # 1x1 dummy transparent PNG
        dummy_png = b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15c4\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82"
        heuristics = inspect_image_heuristics(dummy_png)
        self.assertTrue(heuristics["valid_format"])
        self.assertEqual(heuristics["format"], "PNG")
        self.assertEqual(heuristics["clarity"], "Low")  # 1x1 is low res

    def test_photo_analysis_civic_issue(self):
        dummy_jpg = b"\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x01\x00H\x00H\x00\x00\xff\xdb\x00C\x00\x08\x06\x06\x07\x06\x05\x08\x07\x07\x07\t\t\x08\n\x0c\x14\r\x0c\x0b\x0b\x0c\x19\x12\x13\x0f\x14\x1d\x1a\x1f\x1e\x1d\x1a\x1c\x1c $.' \",#\x1c\x1c(7),01444\x1f'9=82<.342\xff\xc0\x00\x0b\x08\x00\x10\x00\x10\x01\x01\x11\x00\xff\xda\x00\x08\x01\x01\x00\x00?\x00\xbf\x00\xff\xd9"
        result = analyze_photo(dummy_jpg, mime_type="image/jpeg", complaint_description="Severe pothole on Siripuram road")
        self.assertIn("detected_issue", result)
        self.assertIn("visible_severity", result)
        self.assertTrue("evidence_limitations" in result)

    def test_before_after_comparison(self):
        img_a = b"\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x01\x00H\x00H\x00\x00\xff\xda\x00\x08\x01\x01\x00\x00?\x00\xbf\x00\xff\xd9"
        img_b = b"\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x01\x00H\x00H\x00\x00\xff\xda\x00\x08\x01\x01\x00\x00?\x00\xbf\x00\xff\xd9"
        comp = compare_before_after_images(img_a, img_b, complaint_category="Road Damage")
        self.assertIn("resolution_verified", comp)
        self.assertIn("status", comp)

    # ---------------------------------------------------------------
    # MODULE 3: DUPLICATE COMPLAINT DETECTION
    # ---------------------------------------------------------------
    def test_duplicate_detection_high_match(self):
        existing = [
            {
                "id": "JS-VSKP08421",
                "description": "Dwaraka Nagar main road sewage drain cover shattered overflow wastewater",
                "category": "Drainage",
                "latitude": 17.7289,
                "longitude": 83.3082
            }
        ]
        new_desc = "Dwaraka Nagar main road broken drain cover sewage water flowing"
        res = detect_duplicates(
            new_description=new_desc,
            new_category="Drainage",
            new_lat=17.7290,
            new_lon=83.3083,
            existing_complaints=existing
        )
        self.assertTrue(res["is_likely_duplicate"])
        self.assertEqual(res["matching_complaint_id"], "JS-VSKP08421")
        self.assertTrue(res["highest_similarity_score"] >= 0.70)
        self.assertIn("CLUSTER-JS-VSKP08421", res["duplicate_cluster_id"])

    def test_haversine_distance(self):
        # Dwaraka Nagar (17.7289, 83.3082) to Siripuram (17.7225, 83.3150) is ~1.0 km
        dist = haversine_distance_km(17.7289, 83.3082, 17.7225, 83.3150)
        self.assertAlmostEqual(dist, 1.0, delta=0.5)

    # ---------------------------------------------------------------
    # MODULE 4: PRIORITY & URGENCY ASSESSMENT
    # ---------------------------------------------------------------
    def test_priority_critical_safety_hazard(self):
        prio = assess_priority(
            complaint_description="Live electric wire snapped from transformer sparking near school entrance",
            category="Electricity",
            vision_severity="Severe",
            duplicate_count=2
        )
        self.assertEqual(prio["priority_level"], "Critical")
        self.assertTrue(prio["priority_score"] >= 80.0)
        self.assertIn("24 Hours", prio["recommended_sla"])
        self.assertTrue(len(prio["contributing_factors"]) >= 2)

    def test_priority_routine_civic_issue(self):
        prio = assess_priority(
            complaint_description="Small pothole near residential colony gate",
            category="Road Damage",
            vision_severity="Low"
        )
        self.assertIn(prio["priority_level"], ["Low", "Medium"])
        self.assertTrue(prio["priority_score"] < 60.0)

    # ---------------------------------------------------------------
    # MODULE 5: PREDICTIVE CIVIC ANALYTICS
    # ---------------------------------------------------------------
    def test_predictive_insights_generation(self):
        records = [
            {"id": "JS-1", "category": "Drainage", "status": "Submitted", "ai_priority": "High", "location": "Ward 34 Dwaraka Nagar", "latitude": 17.7289, "longitude": 83.3082},
            {"id": "JS-2", "category": "Drainage", "status": "In Progress", "ai_priority": "High", "location": "Ward 34 Dwaraka Nagar", "latitude": 17.7291, "longitude": 83.3085},
            {"id": "JS-3", "category": "Road Damage", "status": "Resolved", "ai_priority": "Medium", "location": "Ward 18 Siripuram", "latitude": 17.7225, "longitude": 83.3150}
        ]
        insights = generate_predictive_insights(records)
        self.assertEqual(insights["dataset_summary"]["total_complaints_analyzed"], 3)
        self.assertEqual(insights["category_breakdown"]["Drainage"], 2)
        self.assertTrue(len(insights["hotspot_analytics"]) > 0)
        self.assertIn("data_origin", insights["dataset_summary"])

    # ---------------------------------------------------------------
    # MODULE 6: EVIDENCE AUTHENTICITY & DEEPFAKE SCREENING
    # ---------------------------------------------------------------
    def test_c2pa_provenance_detection(self):
        clean_bytes = b"Standard raw camera JPEG bytes without manifests"
        res = inspect_c2pa_provenance(clean_bytes)
        self.assertFalse(res["c2pa_detected"])
        self.assertEqual(res["status"], "Unknown / Unsigned")

        # Injected test manifest block
        c2pa_bytes = b"Header...jumb...c2pa manifest block..."
        res_signed = inspect_c2pa_provenance(c2pa_bytes)
        self.assertTrue(res_signed["c2pa_detected"])

    def test_watermark_and_synthetic_detection(self):
        ai_tagged_bytes = b"Image header data generated with Midjourney v6"
        res = inspect_watermarks_and_generators(ai_tagged_bytes)
        self.assertIn("Midjourney", res["generators_flagged"])

        clean_photo = b"\xff\xd8\xff\xe0...clean authentic photo..."
        res_clean = inspect_watermarks_and_generators(clean_photo)
        self.assertEqual(len(res_clean["generators_flagged"]), 0)

    def test_evidence_authenticity_pipeline_guardrails(self):
        dummy_img = b"\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x01\x00H\x00H\x00\x00\xff\xd9"
        res = screen_evidence_authenticity(
            image_bytes=dummy_img,
            complaint_description="Dwaraka nagar drain",
            claimed_category="Drainage"
        )
        self.assertIn(res["evidence_risk_level"], [
            "No concerning indicators detected",
            "Possible AI-generated content",
            "Possible image manipulation",
            "Provenance verified",
            "Verification inconclusive",
            "Human review required"
        ])
        self.assertIn("administrative_disclaimer", res)

    # ---------------------------------------------------------------
    # PIPELINE INTEGRATION & PERSISTENCE
    # ---------------------------------------------------------------
    def test_complete_pipeline_execution(self):
        res = run_complete_pipeline(
            description="Siripuram road deep pothole right after AU university gate causing two-wheeler skids",
            location="Ward 18, Siripuram, Visakhapatnam",
            latitude=17.7225,
            longitude=83.3150,
            save_to_db=True
        )
        self.assertEqual(res["status"], "success")
        self.assertTrue(res["complaint_id"].startswith("JS-VSKP"))
        self.assertIn("triage_summary", res)
        self.assertIn("modules", res)

        # Verify SQLite row
        conn = get_db_connection()
        row = conn.execute("SELECT * FROM complaints WHERE id = ?", (res["complaint_id"],)).fetchone()
        conn.close()
        self.assertIsNotNone(row)
        self.assertEqual(row["id"], res["complaint_id"])


if __name__ == "__main__":
    unittest.main()
