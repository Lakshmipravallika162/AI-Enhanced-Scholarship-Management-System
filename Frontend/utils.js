// utils.js — Shared helpers across all pages

const API_BASE = "http://localhost:5000/api";

function getUser() {
  const u = localStorage.getItem("scholar_user");
  return u ? JSON.parse(u) : null;
}

function logout() {
  localStorage.removeItem("scholar_user");
  window.location.href = "index.html";
}

function requireAuth(role) {
  const user = getUser();
  if (!user) { window.location.href = "index.html"; return null; }
  if (role && user.role !== role) {
    alert("Access denied.");
    window.location.href = "index.html";
    return null;
  }
  const el = document.getElementById("userName");
  if (el) el.textContent = user.name;
  return user;
}

async function apiCall(path, method = "GET", body = null) {
  const opts = { method, headers: { "Content-Type": "application/json" } };
  if (body) opts.body = JSON.stringify(body);
  const res = await fetch(API_BASE + path, opts);
  return res.json();
}

function statusBadge(status) {
  const cls = { Pending: "badge-pending", Approved: "badge-approved", Rejected: "badge-rejected" };
  return `<span class="badge ${cls[status] || ''}">${status}</span>`;
}

function mlBadge(result) {
  if (!result) return `<span class="badge badge-not">Not Predicted</span>`;
  const cls = result === "Eligible" ? "badge-eligible" : "badge-not";
  return `<span class="badge ${cls}">${result}</span>`;
}

function showMsg(id, text, type) {
  const el = document.getElementById(id);
  if (!el) return;
  el.className = `msg ${type}`;
  el.textContent = text;
  el.classList.remove("hidden");
}

function fmtDate(d) {
  if (!d) return "—";
  return new Date(d).toLocaleDateString("en-IN", { day: "2-digit", month: "short", year: "numeric" });
}

function closeModal() {
  const m = document.getElementById("appModal");
  if (m) m.classList.add("hidden");
}
