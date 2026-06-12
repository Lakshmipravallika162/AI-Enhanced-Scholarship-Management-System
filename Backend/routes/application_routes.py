"""
Application Routes: Submit, List, Track Status
"""

from flask import Blueprint, request, jsonify
from models.database import get_db

application_bp = Blueprint("applications", __name__)

# ── Submit Application ─────────────────────────
@application_bp.route("/submit", methods=["POST"])
def submit():
    data = request.get_json()
    required = ["user_id","gpa","attendance_pct","family_income_level",
                "previous_scholarship","extracurricular_score","category_eligible"]

    for field in required:
        if field not in data:
            return jsonify({"error": f"Missing field: {field}"}), 400

    db = get_db()
    cursor = db.execute("""
        INSERT INTO applications
          (user_id, gpa, attendance_pct, family_income_level,
           previous_scholarship, extracurricular_score, category_eligible)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        data["user_id"], data["gpa"], data["attendance_pct"],
        data["family_income_level"], data["previous_scholarship"],
        data["extracurricular_score"], data["category_eligible"]
    ))
    app_id = cursor.lastrowid
    db.commit()
    db.close()

    return jsonify({"message": "Application submitted", "application_id": app_id}), 201

# ── Student: My Applications ───────────────────
@application_bp.route("/my/<int:user_id>", methods=["GET"])
def my_applications(user_id):
    db   = get_db()
    rows = db.execute("""
        SELECT a.*, p.result, p.probability, r.report_text
        FROM applications a
        LEFT JOIN predictions p ON p.application_id = a.id
        LEFT JOIN reports     r ON r.application_id = a.id
        WHERE a.user_id = ?
        ORDER BY a.submitted_at DESC
    """, (user_id,)).fetchall()
    db.close()
    return jsonify([dict(r) for r in rows]), 200

# ── Single Application Details ─────────────────
@application_bp.route("/<int:app_id>", methods=["GET"])
def get_application(app_id):
    db  = get_db()
    row = db.execute("""
        SELECT a.*, u.name AS student_name, u.email AS student_email,
               p.result, p.probability, r.report_text
        FROM applications a
        JOIN users u ON u.id = a.user_id
        LEFT JOIN predictions p ON p.application_id = a.id
        LEFT JOIN reports     r ON r.application_id = a.id
        WHERE a.id = ?
    """, (app_id,)).fetchone()
    db.close()
    if not row:
        return jsonify({"error": "Not found"}), 404
    return jsonify(dict(row)), 200

# ── Admin: Update Status ───────────────────────
@application_bp.route("/<int:app_id>/status", methods=["PUT"])
def update_status(app_id):
    data   = request.get_json()
    status = data.get("status")  # Approved | Rejected

    if status not in ["Approved", "Rejected"]:
        return jsonify({"error": "Status must be Approved or Rejected"}), 400

    db = get_db()
    db.execute("""
        UPDATE applications
        SET status=?, reviewed_at=datetime('now')
        WHERE id=?
    """, (status, app_id))
    db.commit()
    db.close()
    return jsonify({"message": f"Application {status}"}), 200
