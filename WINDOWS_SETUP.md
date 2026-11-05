# JanSakshi AI — Windows PowerShell Execution & Installation Guide

This document provides exact, step-by-step Windows PowerShell instructions to set up, test, and run the **JanSakshi AI** platform locally on Windows.

---

### Prerequisites
- Windows 10 or Windows 11 (64-bit)
- Python 3.10+ installed and added to Windows PATH (`python --version`)
- Node.js (v18+ or v20+) for the frontend static dev server (optional if serving directly from Flask)

---

### Step 1: Open Windows PowerShell in Project Directory
Open PowerShell and navigate to the project directory:
```powershell
cd C:\path\to\jansakshi
```

---

### Step 2: Create and Activate Python Virtual Environment
```powershell
# 1. Create a clean virtual environment
python -m venv venv

# 2. If PowerShell script execution is restricted, allow local scripts:
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

# 3. Activate the virtual environment
.\venv\Scripts\Activate.ps1
```

---

### Step 3: Install Required Python Dependencies
```powershell
python -m pip install --upgrade pip
pip install -r backend\requirements.txt
```

---

### Step 4: Configure Environment Variables
Copy `.env.example` to `.env` or set PowerShell session variables directly:

```powershell
# Option A: Set session environment variables
$env:GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"
$env:GEMINI_MODEL = "gemini-3.8-flash"

# Option B: Create local .env file (never commit your secret key)
if (-not (Test-Path .env)) {
    Copy-Item .env.example .env
}
```

*Note:* If `GEMINI_API_KEY` is not provided, the platform automatically activates deterministic rule-based semantic fallbacks, heuristic image forensics, and full local SQLite persistence without crashing.

---

### Step 5: Run Automated Unit Tests (All 6 AI Modules)
Execute the comprehensive test suite to verify all six modules:
```powershell
python -m unittest backend\tests\test_all_modules.py -v
```

Expected output:
```
test_c2pa_provenance_detection ... ok
test_complete_pipeline_execution ... ok
test_duplicate_detection_high_match ... ok
test_english_complaint_understanding ... ok
test_evidence_authenticity_pipeline_guardrails ... ok
test_haversine_distance ... ok
test_image_heuristics_validation ... ok
test_missing_data_resilience ... ok
test_photo_analysis_civic_issue ... ok
test_predictive_insights_generation ... ok
test_priority_critical_safety_hazard ... ok
test_priority_routine_civic_issue ... ok
test_telugu_transliterated_complaint_understanding ... ok
test_telugu_unicode_complaint_understanding ... ok
test_watermark_and_synthetic_detection ... ok
----------------------------------------------------------------------
Ran 16 tests in 0.02s
OK
```

---

### Step 6: Start the Flask Backend
```powershell
python backend\app.py
```

The Flask server will start on:
```
http://127.0.0.1:5000
```

Verify backend health in another PowerShell tab or browser:
```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:5000/api/health"
```

---

### Step 7: Launch the Application in Browser

Since `backend/app.py` serves the static portal files directly:
- **Citizen Portal & Public Accountability**: `http://127.0.0.1:5000/index.html`
- **Register Grievance**: `http://127.0.0.1:5000/register.html`
- **Track Complaint Docket**: `http://127.0.0.1:5000/track.html`
- **Officer Dashboard**: `http://127.0.0.1:5000/officer.html`

If you are using Vite in parallel:
```powershell
npm run dev
```
Open `http://localhost:3000` (API calls are proxied to port 5000).

---

### Six AI Modules API Quick Reference

| Endpoint | Method | Description |
|---|---|---|
| `/api/health` | GET | Health status and AI module readiness |
| `/api/complaints` | POST | Register complaint |
| `/api/complaints` | GET | List all stored complaints |
| `/api/complaints/<id>` | GET | Track single complaint by tracking token |
| `/api/ai/analyze-complaint` | POST | Module 1: Multilingual understanding (Telugu/English) |
| `/api/ai/analyze-image` | POST | Module 2: Photo analysis & civic defect classification |
| `/api/ai/compare-resolution` | POST | Module 2: Before & After repair comparison |
| `/api/ai/detect-duplicates` | POST | Module 3: Semantic & spatial duplicate clustering |
| `/api/ai/assess-priority` | POST | Module 4: Explainable multi-factor urgency assessment |
| `/api/ai/predictive-insights`| GET | Module 5: Hotspots, ward analytics & pattern recognition |
| `/api/ai/verify-evidence` | POST | Module 6: C2PA, EXIF, watermark & synthetic screening |
| `/api/ai/analyze-complete` | POST | Coordinated 6-module pipeline execution |
