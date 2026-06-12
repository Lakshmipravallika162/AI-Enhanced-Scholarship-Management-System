"""
Admin Routes: Dashboard, All Applications, Analytics
"""

from flask import Blueprint, jsonify
from models.database import get_db

admin_bp = Blueprint("admin", __name__)

# ── Dashboard Summary Stats ────────────────────
@admin_bp.route("/dashboard", methods=["GET"])
def dashboard():
    db = get_db()

    total       = db.execute("SELECT COUNT(*) FROM applications").fetchone()[0]
    pending     = db.execute("SELECT COUNT(*) FROM applications WHERE status='Pending'").fetchone()[0]
    approved    = db.execute("SELECT COUNT(*) FROM applications WHERE status='Approved'").fetchone()[0]
    rejected    = db.execute("SELECT COUNT(*) FROM applications WHERE status='Rejected'").fetchone()[0]
    eligible    = db.execute("SELECT COUNT(*) FROM predictions WHERE result='Eligible'").fetchone()[0]
    not_eligible= db.execute("SELECT COUNT(*) FROM predictions WHERE result='Not Eligible'").fetchone()[0]
    avg_prob    = db.execute("SELECT AVG(probability) FROM predictions").fetchone()[0]
    total_users = db.execute("SELECT COUNT(*) FROM users WHERE role='student'").fetchone()[0]
    db.close()

    return jsonify({
        "total_applications": total,
        "pending":            pending,
        "approved":           approved,
        "rejected":           rejected,
        "ml_eligible":        eligible,
        "ml_not_eligible":    not_eligible,
        "avg_probability":    round(avg_prob or 0, 2),
        "total_students":     total_users
    }), 200


# ── All Applications (with student + prediction info) ──
@admin_bp.route("/applications", methods=["GET"])
def all_applications():
    db   = get_db()
    rows = db.execute("""
        SELECT a.*, u.name AS student_name, u.email AS student_email,
               p.result, p.probability
        FROM applications a
        JOIN users u ON u.id = a.user_id
        LEFT JOIN predictions p ON p.application_id = a.id
        ORDER BY a.submitted_at DESC
    """).fetchall()
    db.close()
    return jsonify([dict(r) for r in rows]), 200


# ── Analytics ─────────────────────────────────
@admin_bp.route("/analytics", methods=["GET"])
def analytics():
    db = get_db()

    # Income level distribution
    income = db.execute("""
        SELECT family_income_level, COUNT(*) as count
        FROM applications GROUP BY family_income_level
    """).fetchall()

    # Avg GPA by status
    avg_gpa = db.execute("""
        SELECT status, ROUND(AVG(gpa),2) as avg_gpa
        FROM applications GROUP BY status
    """).fetchall()

    # Monthly submissions
    monthly = db.execute("""
        SELECT strftime('%Y-%m', submitted_at) as month, COUNT(*) as count
        FROM applications GROUP BY month ORDER BY month
    """).fetchall()

    db.close()
    return jsonify({
        "income_distribution": [dict(r) for r in income],
        "avg_gpa_by_status":   [dict(r) for r in avg_gpa],
        "monthly_submissions": [dict(r) for r in monthly],
    }), 200
