"""
Auth Routes: Register, Login (Student & Admin)
"""

from flask import Blueprint, request, jsonify
from models.database import get_db

auth_bp = Blueprint("auth", __name__)

# ── Register ──────────────────────────────────
@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    name     = data.get("name", "").strip()
    email    = data.get("email", "").strip().lower()
    password = data.get("password", "")
    role     = data.get("role", "student")   # default student

    if not name or not email or not password:
        return jsonify({"error": "All fields are required"}), 400

    db = get_db()
    try:
        db.execute(
            "INSERT INTO users (name, email, password, role) VALUES (?, ?, ?, ?)",
            (name, email, password, role)
        )
        db.commit()
        return jsonify({"message": "Registration successful"}), 201
    except Exception:
        return jsonify({"error": "Email already exists"}), 409
    finally:
        db.close()

# ── Login ─────────────────────────────────────
@auth_bp.route("/login", methods=["POST"])
def login():
    data     = request.get_json()
    email    = data.get("email", "").strip().lower()
    password = data.get("password", "")

    db   = get_db()
    user = db.execute(
        "SELECT * FROM users WHERE email=? AND password=?", (email, password)
    ).fetchone()
    db.close()

    if not user:
        return jsonify({"error": "Invalid credentials"}), 401

    return jsonify({
        "message": "Login successful",
        "user": {
            "id":    user["id"],
            "name":  user["name"],
            "email": user["email"],
            "role":  user["role"]
        }
    }), 200
