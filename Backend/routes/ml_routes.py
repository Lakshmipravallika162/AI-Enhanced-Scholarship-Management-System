"""
ML Routes: Scholarship Eligibility Prediction
Uses trained Logistic Regression model (pickle)
"""

import os, sys
import numpy as np
from flask import Blueprint, request, jsonify
from models.database import get_db
import joblib

ml_bp = Blueprint("ml", __name__)

# Load saved model artifacts
MODEL_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "ML", "saved_model")

try:
    model    = joblib.load(os.path.join(MODEL_DIR, "logistic_model.pkl"))
    scaler   = joblib.load(os.path.join(MODEL_DIR, "scaler.pkl"))
    le       = joblib.load(os.path.join(MODEL_DIR, "label_encoder.pkl"))
    features = joblib.load(os.path.join(MODEL_DIR, "feature_names.pkl"))
    print("✅ ML model loaded")
except Exception as e:
    print(f"⚠️  ML model not found: {e}")
    model = scaler = le = features = None


def encode_income(level: str) -> int:
    """High→0, Low→1, Medium→2 (LabelEncoder order)"""
    mapping = {"High": 0, "Low": 1, "Medium": 2}
    return mapping.get(level, 1)


# ── Predict from raw input ────────────────────
@ml_bp.route("/predict", methods=["POST"])
def predict():
    if model is None:
        return jsonify({"error": "ML model not loaded"}), 500

    data = request.get_json()
    try:
        row = np.array([[
            float(data["gpa"]),
            int(data["attendance_pct"]),
            encode_income(data["family_income_level"]),
            int(data["previous_scholarship"]),
            int(data["extracurricular_score"]),
            int(data["category_eligible"]),
        ]])
        scaled      = scaler.transform(row)
        prediction  = model.predict(scaled)[0]
        probability = round(float(model.predict_proba(scaled)[0][1]) * 100, 2)
        result      = "Eligible" if prediction == 1 else "Not Eligible"

        # Save to DB if application_id provided
        app_id = data.get("application_id")
        if app_id:
            db = get_db()
            db.execute(
                "INSERT OR REPLACE INTO predictions (application_id, result, probability) VALUES (?,?,?)",
                (app_id, result, probability)
            )
            db.commit()
            db.close()

        return jsonify({
            "result":      result,
            "probability": probability,
            "eligible":    bool(prediction == 1)
        }), 200

    except KeyError as e:
        return jsonify({"error": f"Missing field: {e}"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ── Predict directly from saved application ───
@ml_bp.route("/predict/<int:app_id>", methods=["POST"])
def predict_from_application(app_id):
    db  = get_db()
    row = db.execute("SELECT * FROM applications WHERE id=?", (app_id,)).fetchone()
    db.close()

    if not row:
        return jsonify({"error": "Application not found"}), 404

    payload = {
        "gpa":                  row["gpa"],
        "attendance_pct":       row["attendance_pct"],
        "family_income_level":  row["family_income_level"],
        "previous_scholarship": row["previous_scholarship"],
        "extracurricular_score":row["extracurricular_score"],
        "category_eligible":    row["category_eligible"],
        "application_id":       app_id
    }

    with ml_bp.open_resource(""):  # just reuse predict logic
        pass

    # Direct call
    if model is None:
        return jsonify({"error": "ML model not loaded"}), 500

    try:
        inp = np.array([[
            float(payload["gpa"]),
            int(payload["attendance_pct"]),
            encode_income(payload["family_income_level"]),
            int(payload["previous_scholarship"]),
            int(payload["extracurricular_score"]),
            int(payload["category_eligible"]),
        ]])
        scaled      = scaler.transform(inp)
        prediction  = model.predict(scaled)[0]
        probability = round(float(model.predict_proba(scaled)[0][1]) * 100, 2)
        result      = "Eligible" if prediction == 1 else "Not Eligible"

        db = get_db()
        db.execute(
            "INSERT OR REPLACE INTO predictions (application_id, result, probability) VALUES (?,?,?)",
            (app_id, result, probability)
        )
        db.commit()
        db.close()

        return jsonify({"result": result, "probability": probability}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
