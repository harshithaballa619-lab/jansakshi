"""
JanSakshi AI - Database Layer with Safe Migrations
Preserves existing complaint records and dynamically applies additive schema migrations.
"""

import os
import sqlite3
import json
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, "jansakshi.db")


def get_db_connection():
    """Returns a connection to the SQLite database with row_factory enabled."""
    conn = sqlite3.connect(DATABASE, timeout=10.0)
    conn.row_factory = sqlite3.Row
    return conn


def apply_migrations(conn):
    """
    Applies additive migrations safely.
    Checks existing columns using PRAGMA table_info and adds any missing columns.
    Never alters, deletes, or re-creates existing tables with data loss.
    """
    cursor = conn.cursor()

    # 1. Base table (if not exists)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS complaints (
            id TEXT PRIMARY KEY,
            description TEXT NOT NULL,
            category TEXT,
            location TEXT,
            latitude REAL,
            longitude REAL,
            image_path TEXT,
            ai_summary TEXT,
            ai_priority TEXT,
            status TEXT DEFAULT 'Submitted',
            created_at TEXT NOT NULL
        )
    """)

    # 2. Get existing columns
    cursor.execute("PRAGMA table_info(complaints)")
    existing_columns = {row["name"] for row in cursor.fetchall()}

    # 3. Additive columns for Six AI Modules
    additive_columns = {
        "department": "TEXT",
        "detected_language": "TEXT",
        "location_clues": "TEXT",
        "missing_information": "TEXT",
        "followup_question": "TEXT",
        "vision_detected_issue": "TEXT",
        "vision_description": "TEXT",
        "vision_severity": "TEXT",
        "vision_clarity": "TEXT",
        "vision_confidence": "REAL",
        "duplicate_cluster_id": "TEXT",
        "is_duplicate": "INTEGER DEFAULT 0",
        "duplicate_match_id": "TEXT",
        "duplicate_similarity": "REAL",
        "duplicate_reason": "TEXT",
        "priority_score": "REAL",
        "priority_reason": "TEXT",
        "priority_factors": "TEXT",
        "recommended_action": "TEXT",
        "recommended_sla": "TEXT",
        "authenticity_status": "TEXT",
        "provenance_status": "TEXT",
        "watermark_status": "TEXT",
        "metadata_status": "TEXT",
        "manipulation_indicators": "TEXT",
        "synthetic_risk_level": "TEXT",
        "authenticity_confidence": "REAL",
        "human_review_required": "INTEGER DEFAULT 0",
        "raw_ai_analysis": "TEXT"
    }

    for col_name, col_type in additive_columns.items():
        if col_name not in existing_columns:
            cursor.execute(f"ALTER TABLE complaints ADD COLUMN {col_name} {col_type}")

    # 4. Duplicate Clusters table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS duplicate_clusters (
            cluster_id TEXT PRIMARY KEY,
            primary_complaint_id TEXT NOT NULL,
            member_ids TEXT NOT NULL,
            similarity_score REAL,
            category TEXT,
            ward TEXT,
            created_at TEXT NOT NULL
        )
    """)

    # 5. Audit Log table for administrative transparency
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS audit_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            complaint_id TEXT NOT NULL,
            action TEXT NOT NULL,
            officer_name TEXT,
            notes TEXT,
            timestamp TEXT NOT NULL
        )
    """)

    conn.commit()


def seed_demo_complaints_if_empty(conn):
    """
    Seeds baseline demonstration records for Greater Visakhapatnam Municipal Corporation (GVMC)
    only if the complaints table is empty.
    Clearly marks data origin as demonstration.
    """
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) as count FROM complaints")
    row = cursor.fetchone()
    if row and row["count"] > 0:
        return  # Do not touch existing complaints

    sample_complaints = [
        (
            "JS-VSKP08421",
            "Dwaraka Nagar main commercial branch road near RTC Complex junction. The municipal sewage drain cover is shattered and black wastewater is spilling onto the street right opposite the medical shop.",
            "Drainage",
            "Ward 34, Dwaraka Nagar, Visakhapatnam",
            17.7289,
            83.3082,
            None,
            "Chronic sewage drain cover failure causing toxic wastewater overflow near commercial medical shop.",
            "High",
            "GVMC Drainage & Sewage Wing",
            "In Progress",
            "2026-11-03T09:30:00",
            "Sewage Drain Overflow",
            "High",
            0.94,
            "48 Hours",
            "Low Risk (Authentic)",
            "No concerning indicators detected",
            "1.0"
        ),
        (
            "JS-VSKP08422",
            "ద్వారకా నగర్ ఆర్టీసీ కాంప్లెక్స్ ఎదురుగా డ్రైనేజీ కాలువ పగిలి మురుగునీరు రోడ్డుపైకి వస్తోంది. దుర్వాసన చాలా ఎక్కువగా ఉంది.",
            "Drainage",
            "Dwaraka Nagar, RTC Complex, Ward 34",
            17.7291,
            83.3085,
            None,
            "Telugu duplicate report of RTC complex sewage overflow with acute odor and public transit obstruction.",
            "High",
            "GVMC Drainage & Sewage Wing",
            "Submitted",
            "2026-11-03T11:15:00",
            "Sewage Drain Overflow",
            "High",
            0.92,
            "48 Hours",
            "Low Risk (Authentic)",
            "No concerning indicators detected",
            "1.0"
        ),
        (
            "JS-VSKP08310",
            "Siripuram Junction to AU Engineering College road deep potholes developed after pipeline trenching work.",
            "Road Damage",
            "Siripuram Junction, Ward 18",
            17.7225,
            83.3150,
            None,
            "Hazardous asphalt surface depression following trenching excavation near university corridor.",
            "Critical",
            "GVMC Roads & Engineering Wing",
            "Submitted",
            "2026-11-04T08:00:00",
            "Potholes & Road Trenching",
            "Critical",
            0.96,
            "24 Hours",
            "Low Risk (Authentic)",
            "No concerning indicators detected",
            "1.0"
        ),
        (
            "JS-VSKP08295",
            "MVP Colony Sector 4 park entrance streetlights are not turning on for the past 5 consecutive nights.",
            "Street Lighting",
            "MVP Colony Sector 4, Ward 22",
            17.7380,
            83.3420,
            None,
            "Dark street hazard at public park perimeter affecting evening joggers and women commuters.",
            "Medium",
            "GVMC Electrical & Streetlights Wing",
            "Resolved",
            "2026-11-01T18:20:00",
            "Streetlight Failure",
            "Medium",
            0.89,
            "72 Hours",
            "Low Risk (Authentic)",
            "No concerning indicators detected",
            "1.0"
        ),
        (
            "JS-VSKP08150",
            "Gajuwaka Industrial area main road near BHPV gate drinking water supply pipeline leaking heavily since morning.",
            "Water Supply",
            "Gajuwaka BHPV Gate, Ward 65",
            17.6950,
            83.2120,
            None,
            "High volume treated drinking water pipeline rupture inundating road verge in industrial belt.",
            "High",
            "GVMC Water Supply & Distribution",
            "Resolved",
            "2026-10-29T07:45:00",
            "Drinking Water Pipe Rupture",
            "High",
            0.95,
            "24 Hours",
            "Low Risk (Authentic)",
            "No concerning indicators detected",
            "1.0"
        )
    ]

    for c in sample_complaints:
        cursor.execute("""
            INSERT OR IGNORE INTO complaints (
                id, description, category, location, latitude, longitude,
                image_path, ai_summary, ai_priority, department,
                status, created_at, vision_detected_issue, vision_severity,
                vision_confidence, recommended_sla, authenticity_status,
                synthetic_risk_level, raw_ai_analysis
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, c)

    conn.commit()


def initialize_database():
    """Initializes the database with additive migrations and baseline records."""
    conn = get_db_connection()
    apply_migrations(conn)
    seed_demo_complaints_if_empty(conn)
    conn.close()


if __name__ == "__main__":
    initialize_database()
    print("Database initialized and migrated safely.")
