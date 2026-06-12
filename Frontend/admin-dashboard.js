// admin-dashboard.js

requireAuth("admin");

async function loadAdminDashboard() {
  const stats = await apiCall("/admin/dashboard");

  document.getElementById("totalStudents").textContent = stats.total_students;
  document.getElementById("totalApps").textContent     = stats.total_applications;
  document.getElementById("pendingApps").textContent   = stats.pending;
  document.getElementById("approvedApps").textContent  = stats.approved;
  document.getElementById("rejectedApps").textContent  = stats.rejected;
  document.getElementById("avgProb").textContent       = stats.avg_probability + "%";

  // Donut chart (SVG)
  renderDonut(stats.ml_eligible, stats.ml_not_eligible);

  // Income bar chart
  const analytics = await apiCall("/admin/analytics");
  renderIncomeChart(analytics.income_distribution);

  // Pending table
  const apps = await apiCall("/admin/applications");
  renderPendingTable(apps.filter(a => a.status === "Pending").slice(0, 8));
}

function renderDonut(eligible, notEligible) {
  const total = eligible + notEligible || 1;
  const pct   = Math.round((eligible / total) * 100);
  const circumference = 2 * Math.PI * 54;
  const dash = (eligible / total) * circumference;

  document.getElementById("donutChart").innerHTML = `
    <svg width="160" height="160" viewBox="0 0 120 120">
      <circle cx="60" cy="60" r="54" fill="none" stroke="#E2E8F0" stroke-width="14"/>
      <circle cx="60" cy="60" r="54" fill="none" stroke="#2563EB" stroke-width="14"
        stroke-dasharray="${dash} ${circumference}" stroke-dashoffset="${circumference/4}"
        stroke-linecap="round" transform="rotate(-90 60 60)"/>
      <text x="60" y="56" text-anchor="middle" font-size="18" font-weight="700" fill="#1E293B">${pct}%</text>
      <text x="60" y="72" text-anchor="middle" font-size="9" fill="#64748B">Eligible</text>
    </svg>
    <div style="display:flex;gap:16px;font-size:13px">
      <span><span style="color:#2563EB">●</span> Eligible: <strong>${eligible}</strong></span>
      <span><span style="color:#E2E8F0">●</span> Not: <strong>${notEligible}</strong></span>
    </div>
  `;
}

function renderIncomeChart(data) {
  const maxVal = Math.max(...data.map(d => d.count), 1);
  document.getElementById("incomeChart").innerHTML = data.map(d => `
    <div class="bar-row">
      <span class="bar-label">${d.family_income_level}</span>
      <div class="bar">
        <div class="bar-inner" style="width:${(d.count / maxVal) * 100}%">${d.count}</div>
      </div>
    </div>
  `).join("");
}

function renderPendingTable(apps) {
  const el = document.getElementById("pendingTable");
  if (!apps.length) {
    el.innerHTML = `<p class="empty-state">No pending applications 🎉</p>`;
    return;
  }
  el.innerHTML = `
    <table>
      <thead><tr>
        <th>ID</th><th>Student</th><th>GPA</th><th>ML Result</th><th>Probability</th><th>Action</th>
      </tr></thead>
      <tbody>
        ${apps.map(a => `
          <tr>
            <td>#${a.id}</td>
            <td>${a.student_name}<br><small>${a.student_email}</small></td>
            <td>${a.gpa}</td>
            <td>${mlBadge(a.result)}</td>
            <td>${a.probability ? a.probability + "%" : "—"}</td>
            <td>
              <a href="admin-applications.html" class="btn btn-sm btn-primary">Review</a>
            </td>
          </tr>
        `).join("")}
      </tbody>
    </table>
  `;
}

loadAdminDashboard();
