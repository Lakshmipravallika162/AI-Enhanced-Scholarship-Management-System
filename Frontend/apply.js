// apply.js

let currentAppId   = null;
let currentResult  = null;
let currentProbability = null;

const user = requireAuth("student");

document.getElementById("applyForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const btn = e.target.querySelector("button[type=submit]");
  btn.disabled = true;
  btn.textContent = "⏳ Submitting...";

  const payload = {
    user_id:               user.id,
    gpa:                   parseFloat(document.getElementById("gpa").value),
    attendance_pct:        parseInt(document.getElementById("attendance").value),
    family_income_level:   document.getElementById("incomeLevel").value,
    previous_scholarship:  parseInt(document.querySelector('input[name="prevSchol"]:checked').value),
    extracurricular_score: parseInt(document.getElementById("extraScore").value),
    category_eligible:     parseInt(document.getElementById("categoryEligible").value),
  };

  try {
    // 1. Submit application
    const subRes = await apiCall("/applications/submit", "POST", payload);
    if (!subRes.application_id) throw new Error(subRes.error || "Submission failed");
    currentAppId = subRes.application_id;

    // 2. Run ML prediction
    const predPayload = { ...payload, application_id: currentAppId };
    const predRes = await apiCall("/ml/predict", "POST", predPayload);

    currentResult      = predRes.result;
    currentProbability = predRes.probability;

    showPredictionResult(predRes.result, predRes.probability);
    btn.textContent = "✅ Submitted";

  } catch (err) {
    alert("Error: " + err.message);
    btn.disabled = false;
    btn.textContent = "Submit Application & Get AI Prediction";
  }
});

function showPredictionResult(result, probability) {
  const panel = document.getElementById("resultPanel");
  panel.classList.remove("hidden");

  const badge = document.getElementById("resultBadge");
  if (result === "Eligible") {
    badge.textContent = "✅ You are ELIGIBLE for the Scholarship!";
    badge.className = "result-badge eligible";
  } else {
    badge.textContent = "❌ Not Eligible at this time";
    badge.className = "result-badge not-eligible";
  }

  const fill = document.getElementById("probFill");
  fill.style.width = probability + "%";
  document.getElementById("probText").textContent = probability + "%";

  panel.scrollIntoView({ behavior: "smooth" });
}

async function getExplanation() {
  if (!currentResult) return;

  const btn = event.target;
  btn.disabled  = true;
  btn.textContent = "⏳ Generating AI explanation...";

  try {
    const res = await apiCall("/genai/explain", "POST", {
      result:      currentResult,
      probability: currentProbability
    });

    const box = document.getElementById("explanationBox");
    box.classList.remove("hidden");
    document.getElementById("explanationText").textContent = res.explanation || res.error;
    btn.textContent = "✅ Explanation Generated";
  } catch {
    btn.textContent = "Generate AI Explanation";
    btn.disabled = false;
  }
}
