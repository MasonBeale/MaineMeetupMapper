const API_BASE = "http://127.0.0.1:5000";

export async function apiRegister(body) {
  const res = await fetch(`${API_BASE}/api/register`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    credentials: "include",
    body: JSON.stringify(body),
  });
  return res.json();
}

export async function apiLogin(body) {
  const res = await fetch(`${API_BASE}/api/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    credentials: "include",
    body: JSON.stringify(body),
  });
  return res.json();
}

export async function apiLogout() {
  await fetch(`${API_BASE}/api/logout`, {
    method: "POST",
    credentials: "include",
  });
}

export async function apiMe() {
  const res = await fetch(`${API_BASE}/api/me`, {
    method: "GET",
    credentials: "include",
  });
  if (!res.ok) return null;
  return res.json();
}

export async function apiUpdateMe(body) {
  const res = await fetch(`${API_BASE}/api/me`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    credentials: "include",
    body: JSON.stringify(body),
  });
  return res.json();
}