"""
Backend Entry Point - AI-Enhanced Scholarship Management System
Flask REST API with ML + GenAI integration
"""

from flask import Flask
from flask_cors import CORS
from routes.auth_routes import auth_bp
from routes.application_routes import application_bp
from routes.ml_routes import ml_bp
from routes.genai_routes import genai_bp
from routes.admin_routes import admin_bp
from models.database import init_db

app = Flask(__name__)
app.secret_key = "scholarship_secret_2025"
CORS(app)

# Register blueprints
app.register_blueprint(auth_bp,        url_prefix="/api/auth")
app.register_blueprint(application_bp, url_prefix="/api/applications")
app.register_blueprint(ml_bp,          url_prefix="/api/ml")
app.register_blueprint(genai_bp,       url_prefix="/api/genai")
app.register_blueprint(admin_bp,       url_prefix="/api/admin")

@app.route("/")
def index():
    return {"message": "Scholarship Management API is running", "version": "1.0"}

if __name__ == "__main__":
    init_db()
    app.run(debug=True, port=5000)
