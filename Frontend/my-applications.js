// my-applications.js

const user = requireAuth("student");

async function loadMyApps() {
  const apps = await apiCall(`/applications/my/${user.id}`);
  const container = document.getElementById("applicationsList");

  if (!Array.isArray(apps) || apps.length === 0) {
    container.innerHTML = `<p class="empty-state">No applications found. <a href="apply.html">Apply now →</a></p>`;
    return;
  }

  container.innerHTML = apps.map(a => `
    <div class="app-card ${a.status.toLowerCase()}">
      <div class="app-card-info">
        <h4>Application #${a.id}
          ${statusBadge(a.status)}
          ${mlBadge(a.result)}
        </h4>
        <p>GPA: <strong>${a.gpa}</strong> | Attendance: <strong>${a.attendance_pct}%</strong> |
           Income: <strong>${a.family_income_level}</strong></p>
        <p>Submitted: ${fmtDate(a.submitted_at)}
          ${a.reviewed_at ? ` | Reviewed: ${fmtDate(a.reviewed_at)}` : ""}
        </p>
        ${a.probability ? `<p>ML Probability: <strong>${a.probability}%</strong></p>` : ""}
      </div>
      <div class="app-card-actions">
        <button class="btn btn-sm btn-secondary" onclick="viewDetails(${a.id})">View Details</button>
      </div>
    </div>
  `).join("");
}

async function viewDetails(appId) {
  const app = await apiCall(`/applications/${appId}`);
  const modal = document.getElementById("appModal");
  const content = document.getElementById("modalContent");

  content.innerHTML = `
    <div class="detail-grid">
      <div class="detail-item"><label>Application ID</label><span>#${app.id}</span></div>
      <div class="detail-item"><label>Status</label><span>${statusBadge(app.status)}</span></div>
      <div class="detail-item"><label>GPA</label><span>${app.gpa} / 4.0</span></div>
      <div class="detail-item"><label>Attendance</label><span>${app.attendance_pct}%</span></div>
      <div class="detail-item"><label>Income Level</label><span>${app.family_income_level}</span></div>
      <div class="detail-item"><label>Category Eligible</label><span>${app.category_eligible ? "Yes" : "No"}</span></div>
      <div class="detail-item"><label>Previous Scholarship</label><span>${app.previous_scholarship ? "Yes" : "No"}</span></div>
      <div class="detail-item"><label>Extracurricular Score</label><span>${app.extracurricular_score}/10</span></div>
      <div class="detail-item"><label>ML Prediction</label><span>${mlBadge(app.result)}</span></div>
      <div class="detail-item"><label>Probability</label><span>${app.probability ? app.probability + "%" : "—"}</span></div>
      <div class="detail-item"><label>Submitted</label><span>${fmtDate(app.submitted_at)}</span></div>
      <div class="detail-item"><label>Reviewed</label><span>${fmtDate(app.reviewed_at)}</span></div>
    </div>
    ${app.report_text ? `
      <h4>📄 AI Evaluation Report</h4>
      <div class="report-box">${app.report_text}</div>
    ` : ""}
  `;

  modal.classList.remove("hidden");
}

loadMyApps();
