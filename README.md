# 🎓 AI-Enhanced Scholarship Management System

> A full-stack web application with Machine Learning + Generative AI integration  
> Built for: Gradious | Algorithm: Logistic Regression | GenAI: Claude API

---

## 📁 Project Structure

```
ScholarshipMS/
├── Frontend/               ← HTML, CSS, JavaScript (UI)
│   ├── index.html          ← Login / Register page
│   ├── css/style.css       ← Complete design system
│   ├── js/                 ← JavaScript logic per page
│   └── pages/              ← All HTML pages
│       ├── student-dashboard.html
│       ├── apply.html
│       ├── my-applications.html
│       ├── admin-dashboard.html
│       └── admin-applications.html
│
├── Backend/                ← Flask REST API
│   ├── app.py              ← Entry point (run this)
│   ├── requirements.txt
│   ├── models/
│   │   └── database.py     ← SQLite setup & schema
│   └── routes/
│       ├── auth_routes.py       ← Register / Login
│       ├── application_routes.py← Submit, track, update
│       ├── ml_routes.py         ← Logistic Regression predict
│       ├── genai_routes.py      ← Claude AI reports
│       └── admin_routes.py      ← Dashboard, analytics
│
└── ML/                     ← Machine Learning module
    ├── train_model.py       ← Data gen + training script
    ├── dataset/
    │   └── scholarship_dataset.csv
    └── saved_model/
        ├── logistic_model.pkl
        ├── scaler.pkl
        ├── label_encoder.pkl
        └── feature_names.pkl
```

---

## 🚀 Setup & Run Instructions

### Step 1 — ML Model Training
```bash
cd ML
python train_model.py
# Outputs: saved_model/*.pkl  (accuracy ~77%)
```

### Step 2 — Backend (Flask)
```bash
cd Backend
pip install -r requirements.txt
export ANTHROPIC_API_KEY="your_api_key_here"   # For GenAI features
python app.py
# Runs on http://localhost:5000
```

### Step 3 — Frontend
Open `Frontend/index.html` in a browser  
Or serve with VS Code Live Server (recommended)

### Default Admin Login
```
Email:    admin@scholarship.com
Password: admin123
```

---

## 🧠 Machine Learning Module

**Task:** Scholarship Eligibility Prediction  
**Algorithm:** Logistic Regression (scikit-learn)  
**Input Features:**
| Feature | Description |
|---|---|
| GPA | Academic performance (0–4.0) |
| Attendance % | Class attendance percentage |
| Family Income Level | Low / Medium / High |
| Previous Scholarship | 0 = No, 1 = Yes |
| Extracurricular Score | 0–10 scale |
| Category Eligible | SC/ST/OBC/EWS = 1 |

**Output:** Eligible / Not Eligible + Probability (%)  
**Evaluation:** Accuracy ~77%, saved as pickle file

---

## 🤖 Generative AI Module

**Task:** Scholarship Explanation & Report Generator  
**Model:** claude-sonnet-4-6 (Anthropic)  
**Features:**
- Eligibility justification report per student
- Strengths & areas of concern breakdown  
- Admin-friendly recommendation
- Student guidance with next steps

**Example Output:**
> "The student is eligible for the scholarship based on strong academic performance (GPA: 3.8), consistent attendance (92%), and low financial background. The system indicates a high probability of approval (87%)..."

---

## 🌐 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/auth/register` | Student registration |
| POST | `/api/auth/login` | Login (student/admin) |
| POST | `/api/applications/submit` | Submit application |
| GET  | `/api/applications/my/:id` | Student's applications |
| PUT  | `/api/applications/:id/status` | Approve/Reject |
| POST | `/api/ml/predict` | Run ML prediction |
| POST | `/api/genai/report/:id` | Generate AI report |
| GET  | `/api/admin/dashboard` | Admin stats |
| GET  | `/api/admin/applications` | All applications |
| GET  | `/api/admin/analytics` | Charts data |

---

## 🛠 Technology Stack

| Layer | Technology |
|---|---|
| Frontend | HTML5, CSS3, Vanilla JavaScript |
| Backend | Python, Flask, Flask-CORS |
| Database | SQLite (via sqlite3) |
| Machine Learning | scikit-learn (Logistic Regression) |
| Generative AI | Anthropic Claude API |
| Model Storage | joblib / pickle |

---

## 📊 Evaluation Criteria Coverage

- ✅ Application functionality (full CRUD workflow)
- ✅ Machine Learning implementation (Logistic Regression, trained & saved)
- ✅ Generative AI output quality (structured 5-section reports)
- ✅ Integration of all modules (ML + GenAI into Flask backend)
- ✅ Code quality and structure (modular routes, blueprints)
- ✅ Project explanation (this README + demo video guide)

---

## 🎥 Demo Video Guide (5–10 mins)

1. Show project folder structure and explain each folder
2. Run `train_model.py` — show metrics output
3. Start Flask backend — show API running
4. Open frontend — register as student
5. Submit a scholarship application
6. Show ML prediction result + probability bar
7. Generate AI explanation
8. Login as Admin — show dashboard stats & charts
9. Open application — run ML prediction, generate AI report
10. Approve / Reject application — student sees update

---

*Submitted by: [Your Name] | Project: AI-Enhanced Scholarship Management System*
