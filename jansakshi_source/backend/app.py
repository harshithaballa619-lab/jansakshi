import os
import sqlite3
import uuid
from datetime import datetime

from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables before importing AI service
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

from ai_service import analyze_complaint

# ---------------------------------
# FLASK CONFIGURATION
# ---------------------------------

app = Flask(__name__)
CORS(app)

DATABASE = os.path.join(BASE_DIR, "jansakshi.db")


# ---------------------------------
# DATABASE CONNECTION
# ---------------------------------

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def initialize_database():
    conn = get_db_connection()

    conn.execute("""
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

    conn.commit()
    conn.close()


# ---------------------------------
# HOME ROUTE
# ---------------------------------

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "project": "JanSakshi AI",
        "message": "Backend is running!",
        "status": "success"
    })


# ---------------------------------
# HEALTH CHECK
# ---------------------------------

@app.route("/api/health", methods=["GET"])
def health():

    try:
        conn = get_db_connection()
        conn.execute("SELECT 1")
        conn.close()

        database_status = "connected"

    except Exception:
        database_status = "error"

    return jsonify({
        "project": "JanSakshi AI",
        "backend": "online",
        "database": database_status,
        "gemini_configured": bool(os.getenv("GEMINI_API_KEY")),
        "gemini_model": os.getenv(
            "GEMINI_MODEL", "gemini-2.5-flash"
        )
    })


# ---------------------------------
# REGISTER A COMPLAINT
# ---------------------------------

@app.route("/api/complaints", methods=["POST"])
def register_complaint():

    data = request.get_json(silent=True) or {}

    description = (data.get("description") or "").strip()

    if not description:
        return jsonify({
            "success": False,
            "error": "Complaint description is required"
        }), 400

    complaint_id = "JS-" + uuid.uuid4().hex[:8].upper()

    created_at = datetime.now().isoformat(timespec="seconds")

    conn = get_db_connection()

    conn.execute("""
        INSERT INTO complaints (
            id,
            description,
            category,
            location,
            latitude,
            longitude,
            image_path,
            ai_summary,
            ai_priority,
            status,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        complaint_id,
        description,
        data.get("category"),
        data.get("location"),
        data.get("latitude"),
        data.get("longitude"),
        data.get("image_path"),
        None,
        None,
        "Submitted",
        created_at
    ))

    conn.commit()
    conn.close()

    return jsonify({
        "success": True,
        "message": "Complaint registered successfully",
        "complaint_id": complaint_id,
        "status": "Submitted"
    }), 201


# ---------------------------------
# GET ALL COMPLAINTS
# ---------------------------------

@app.route("/api/complaints", methods=["GET"])
def get_complaints():

    conn = get_db_connection()

    rows = conn.execute("""
        SELECT * FROM complaints
        ORDER BY created_at DESC
    """).fetchall()

    conn.close()

    return jsonify({
        "success": True,
        "complaints": [dict(row) for row in rows]
    })


# ---------------------------------
# TRACK A COMPLAINT
# ---------------------------------

@app.route("/api/complaints/<complaint_id>", methods=["GET"])
def get_complaint(complaint_id):

    conn = get_db_connection()

    row = conn.execute("""
        SELECT * FROM complaints
        WHERE id = ?
    """, (complaint_id,)).fetchone()

    conn.close()

    if row is None:
        return jsonify({
            "success": False,
            "error": "Complaint not found"
        }), 404

    return jsonify({
        "success": True,
        "complaint": dict(row)
    })


# ---------------------------------
# GEMINI AI COMPLAINT ANALYSIS
# ---------------------------------

@app.route("/api/ai/analyze-complaint", methods=["POST"])
@app.route("/api/analyze", methods=["POST"])
def ai_analyze_complaint():

    data = request.get_json(silent=True) or {}

    description = (data.get("description") or "").strip()
    location = data.get("location")

    if not description:
        return jsonify({
            "success": False,
            "error": "Complaint description is required"
        }), 400

    try:
        analysis = analyze_complaint(
            description=description,
            location=location
        )

        return jsonify({
            "success": True,
            "analysis": analysis
        }), 200

    except Exception as e:

        app.logger.exception("AI complaint analysis failed")

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# ---------------------------------
# START SERVER
# ---------------------------------

initialize_database()

if __name__ == "__main__":

    print("========================================")
    print("          JANSAKSHI AI BACKEND")
    print("========================================")
    print("Database initialized.")
    print("Gemini configured:", bool(os.getenv("GEMINI_API_KEY")))
    print("Starting server: http://127.0.0.1:5000")

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )