// admin-applications.js

requireAuth("admin");

let allApps = [];

async function loadAllApps() {
  allApps = await apiCall("/admin/applications");
  renderApps(allApps);
}

function filterApps() {
  const status  = document.getElementById("statusFilter").value;
  const search  = document.getElementById("searchInput").value.toLowerCase();
  const filtered = allApps.filter(a => {
    const matchStatus = status === "all" || a.status === status;
    const matchSearch = a.student_name.toLowerCase().includes(search) ||
                        a.student_email.toLowerCase().includes(search);
    return matchStatus && matchSearch;
  });
  renderApps(filtered);
}

function renderApps(apps) {
  const el = document.getElementById("appTable");
  if (!apps.length) {
    el.innerHTML = `<p class="empty-state">No applications found.</p>`;
    return;
  }
  el.innerHTML = `
    <table>
      <thead><tr>
        <th>ID</th><th>Student</th><th>GPA</th><th>Att%</th>
        <th>Income</th><th>ML Result</th><th>Prob%</th>
        <th>Status</th><th>Actions</th>
      </tr></thead>
      <tbody>
        ${apps.map(a => `
          <tr>
            <td>#${a.id}</td>
            <td><strong>${a.student_name}</strong><br><small>${a.student_email}</small></td>
            <td>${a.gpa}</td>
            <td>${a.attendance_pct}%</td>
            <td>${a.family_income_level}</td>
            <td>${mlBadge(a.result)}</td>
            <td>${a.probability ? a.probability + "%" : "—"}</td>
            <td>${statusBadge(a.status)}</td>
            <td>
              <button class="btn btn-sm btn-secondary" onclick="viewApp(${a.id})">Review</button>
            </td>
          </tr>
        `).join("")}
      </tbody>
    </table>
  `;
}

async function viewApp(appId) {
  const app = await apiCall(`/applications/${appId}`);
  const modal   = document.getElementById("appModal");
  const content = document.getElementById("modalContent");

  content.innerHTML = `
    <h3>Application #${app.id} — ${app.student_name}</h3>
    <p style="color:var(--text-muted);margin-bottom:16px">${app.student_email}</p>
    <div class="detail-grid">
      <div class="detail-item"><label>GPA</label><span>${app.gpa} / 4.0</span></div>
      <div class="detail-item"><label>Attendance</label><span>${app.attendance_pct}%</span></div>
      <div class="detail-item"><label>Income Level</label><span>${app.family_income_level}</span></div>
      <div class="detail-item"><label>Category Eligible</label><span>${app.category_eligible ? "Yes" : "No"}</span></div>
      <div class="detail-item"><label>Prev Scholarship</label><span>${app.previous_scholarship ? "Yes" : "No"}</span></div>
      <div class="detail-item"><label>Extracurricular</label><span>${app.extracurricular_score}/10</span></div>
      <div class="detail-item"><label>ML Prediction</label><span>${mlBadge(app.result)}</span></div>
      <div class="detail-item"><label>Probability</label><span>${app.probability ? app.probability + "%" : "—"}</span></div>
      <div class="detail-item"><label>Current Status</label><span>${statusBadge(app.status)}</span></div>
      <div class="detail-item"><label>Submitted</label><span>${fmtDate(app.submitted_at)}</span></div>
    </div>

    <div style="display:flex;gap:10px;margin-bottom:16px;flex-wrap:wrap">
      ${!app.result ? `
        <button class="btn btn-secondary" onclick="runMLPredict(${appId})">
          🤖 Run ML Prediction
        </button>
      ` : ""}
      <button class="btn btn-secondary" onclick="generateReport(${appId})">
        📄 Generate AI Report
      </button>
      ${app.status === "Pending" ? `
        <button class="btn btn-success" onclick="updateStatus(${appId}, 'Approved')">✅ Approve</button>
        <button class="btn btn-danger"  onclick="updateStatus(${appId}, 'Rejected')">❌ Reject</button>
      ` : ""}
    </div>

    <div id="reportArea">
      ${app.report_text
        ? `<h4>📄 AI Report</h4><div class="report-box">${app.report_text}</div>`
        : `<p style="color:var(--text-muted);font-size:13px">No AI report yet. Click "Generate AI Report" above.</p>`
      }
    </div>
  `;

  modal.classList.remove("hidden");
}

async function runMLPredict(appId) {
  const btn = event.target;
  btn.disabled = true; btn.textContent = "⏳ Running...";
  const res = await apiCall(`/ml/predict/${appId}`, "POST");
  btn.textContent = `🤖 Result: ${res.result} (${res.probability}%)`;
  loadAllApps();
}

async function generateReport(appId) {
  const btn = event.target;
  btn.disabled = true; btn.textContent = "⏳ Generating with AI...";
  const res = await apiCall(`/genai/report/${appId}`, "POST");
  document.getElementById("reportArea").innerHTML =
    `<h4>📄 AI Report</h4><div class="report-box">${res.report || res.error}</div>`;
  btn.textContent = "✅ Report Generated";
}

async function updateStatus(appId, status) {
  if (!confirm(`${status} this application?`)) return;
  await apiCall(`/applications/${appId}/status`, "PUT", { status });
  closeModal();
  loadAllApps();
}

loadAllApps();
