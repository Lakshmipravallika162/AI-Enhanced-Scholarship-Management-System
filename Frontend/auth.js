// auth.js

const API_BASE = "http://localhost:5000/api";

function switchTab(tab) {
  document.getElementById("loginForm").classList.toggle("hidden", tab !== "login");
  document.getElementById("registerForm").classList.toggle("hidden", tab !== "register");
  document.querySelectorAll(".tab-btn").forEach((b, i) => {
    b.classList.toggle("active", (i === 0 && tab === "login") || (i === 1 && tab === "register"));
  });
  document.getElementById("authMsg").classList.add("hidden");
}

document.getElementById("loginForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const email    = document.getElementById("loginEmail").value;
  const password = document.getElementById("loginPass").value;

  try {
    const res  = await fetch(`${API_BASE}/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password })
    });
    const data = await res.json();

    if (res.ok) {
      localStorage.setItem("scholar_user", JSON.stringify(data.user));
      if (data.user.role === "admin") {
        window.location.href = "admin-dashboard.html";
      } else {
        window.location.href = "student-dashboard.html";
      }
    } else {
      showAuthMsg(data.error || "Login failed", "error");
    }
  } catch {
    showAuthMsg("Cannot connect to server. Is backend running on port 5000?", "error");
  }
});

document.getElementById("registerForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const name     = document.getElementById("regName").value;
  const email    = document.getElementById("regEmail").value;
  const password = document.getElementById("regPass").value;

  try {
    const res  = await fetch(`${API_BASE}/auth/register`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name, email, password, role: "student" })
    });
    const data = await res.json();

    if (res.ok) {
      showAuthMsg("Account created! Please login.", "success");
      switchTab("login");
    } else {
      showAuthMsg(data.error || "Registration failed", "error");
    }
  } catch {
    showAuthMsg("Cannot connect to server", "error");
  }
});

function showAuthMsg(text, type) {
  const el = document.getElementById("authMsg");
  el.className = `msg ${type}`;
  el.textContent = text;
  el.classList.remove("hidden");
}
