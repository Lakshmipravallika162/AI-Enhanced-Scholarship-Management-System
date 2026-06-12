// student-dashboard.js

const user = requireAuth("student");
document.getElementById("welcomeName").textContent = user.name;

async function loadDashboard() {
  const apps = await apiCall(`/applications/my/${user.id}`);
  if (!Array.isArray(apps)) return;

  document.getElementById("totalApps").textContent    = apps.length;
  document.getElementById("approvedApps").textContent = apps.filter(a => a.status === "Approved").length;
  document.getElementById("pendingApps").textContent  = apps.filter(a => a.status === "Pending").length;
  document.getElementById("rejectedApps").textContent = apps.filter(a => a.status === "Rejected").length;

  const container = document.getElementById("recentApps");
  if (apps.length === 0) {
    container.innerHTML = `<p class="empty-state">No applications yet. <a href="apply.html">Apply now →</a></p>`;
    return;
  }

  container.innerHTML = apps.slice(0, 5).map(a => `
    <div class="app-card ${a.status.toLowerCase()}">
      <div class="app-card-info">
        <h4>Application #${a.id}</h4>
        <p>GPA: ${a.gpa} | Attendance: ${a.attendance_pct}% | Income: ${a.family_income_level}</p>
        <p>Submitted: ${fmtDate(a.submitted_at)}</p>
      </div>
      <div class="app-card-actions">
        ${statusBadge(a.status)}
        ${mlBadge(a.result)}
        ${a.probability ? `<small>${a.probability}% probability</small>` : ""}
      </div>
    </div>
  `).join("");
}

loadDashboard();
