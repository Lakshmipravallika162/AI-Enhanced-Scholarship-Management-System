"""
GenAI Routes: Scholarship Explanation & Report Generator
Uses Anthropic Claude API for natural language explanations
"""

import os
import requests
from flask import Blueprint, request, jsonify
from models.database import get_db

genai_bp = Blueprint("genai", __name__)

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
CLAUDE_MODEL      = "claude-sonnet-4-6"


def call_claude(prompt: str) -> str:
    """Call Claude API and return text response."""
    headers = {
        "x-api-key":         ANTHROPIC_API_KEY,
        "anthropic-version": "2023-06-01",
        "content-type":      "application/json",
    }
    body = {
        "model":      CLAUDE_MODEL,
        "max_tokens": 1024,
        "messages":   [{"role": "user", "content": prompt}]
    }
    resp = requests.post(
        "https://api.anthropic.com/v1/messages",
        headers=headers, json=body, timeout=30
    )
    resp.raise_for_status()
    return resp.json()["content"][0]["text"]


def build_prompt(app_data: dict, result: str, probability: float) -> str:
    """Craft a structured prompt for the LLM."""
    return f"""
You are a Scholarship Evaluation AI assistant for an educational institution.
Generate a clear, professional, and empathetic scholarship evaluation report.

Student Application Details:
- GPA / Academic Score  : {app_data['gpa']} / 4.0
- Attendance Percentage : {app_data['attendance_pct']}%
- Family Income Level   : {app_data['family_income_level']}
- Previous Scholarship  : {'Yes' if app_data['previous_scholarship'] else 'No'}
- Extracurricular Score : {app_data['extracurricular_score']} / 10
- Category Eligible     : {'Yes' if app_data['category_eligible'] else 'No'}

ML Prediction Result    : {result}
Approval Probability    : {probability}%

Generate a report with the following sections:
1. **Eligibility Summary** – One paragraph stating if the student is eligible and why.
2. **Strengths** – Bullet points of strong academic/personal factors.
3. **Areas of Concern** – Bullet points of weak factors (if any).
4. **Admin Recommendation** – Suggest approval/rejection with reasoning.
5. **Student Guidance** – Encouraging note with actionable next steps.

Keep the tone professional, fair, and supportive. Be specific to the data provided.
"""


# ── Generate Report for Application ───────────
@genai_bp.route("/report/<int:app_id>", methods=["POST"])
def generate_report(app_id):
    if not ANTHROPIC_API_KEY:
        return jsonify({"error": "ANTHROPIC_API_KEY not configured"}), 500

    db  = get_db()
    row = db.execute("""
        SELECT a.*, p.result, p.probability
        FROM applications a
        LEFT JOIN predictions p ON p.application_id = a.id
        WHERE a.id = ?
    """, (app_id,)).fetchone()

    if not row:
        db.close()
        return jsonify({"error": "Application not found"}), 404

    app_data    = dict(row)
    result      = app_data.get("result", "Not Predicted")
    probability = app_data.get("probability", 0)

    try:
        prompt      = build_prompt(app_data, result, probability)
        report_text = call_claude(prompt)

        # Save to DB
        db.execute(
            "INSERT OR REPLACE INTO reports (application_id, report_text) VALUES (?,?)",
            (app_id, report_text)
        )
        db.commit()
        db.close()

        return jsonify({"report": report_text, "application_id": app_id}), 200

    except Exception as e:
        db.close()
        return jsonify({"error": str(e)}), 500


# ── Quick Explain (no DB needed) ──────────────
@genai_bp.route("/explain", methods=["POST"])
def explain():
    if not ANTHROPIC_API_KEY:
        return jsonify({"error": "ANTHROPIC_API_KEY not configured"}), 500

    data   = request.get_json()
    result = data.get("result", "Unknown")
    prob   = data.get("probability", 0)

    prompt = f"""
In 3-4 sentences, explain to a student why they received the scholarship prediction: '{result}' 
with a probability of {prob}%. Be encouraging, clear, and specific.
"""
    try:
        explanation = call_claude(prompt)
        return jsonify({"explanation": explanation}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
