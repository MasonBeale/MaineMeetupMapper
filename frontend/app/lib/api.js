const API_BASE = "http://127.0.0.1:5000";

export async function apiRegister({ username, email, password }) {
    const res = await fetch(`${API_BASE}/api/register`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      credentials: "include",
      body: JSON.stringify({ username, email, password }),
    });
    const data = await res.json();
    return data; 
  }

  export async function apiLogin({ username, password }) {
    const res = await fetch(`${API_BASE}/api/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      credentials: "include",          
      body: JSON.stringify({ username, password }),
    });
    
    const data = await res.json().catch(() => ({ error: "Login failed" }));
    if (!res.ok) return { error: data.error || "Login failed" };
    return data;
  }

  export async function apiLogout() {
    const res = await fetch(`${API_BASE}/api/logout`, {
      method: "POST",
      credentials: "include",            
    });
    return res.json();
  }

export async function apiMe() {
  try {
    const res = await fetch(`${API_BASE}/api/me`, {
      method: "GET",
      credentials: "include",
    });
    console.log("apiMe status:", res.status);
    const data = await res.json();
    console.log("apiMe data:", data);
    return data.user || null;
  } catch (e) {
    console.error("apiMe fetch error:", e);
    return null;
  }
}

export async function apiUpdateMe(payload) {
  const res = await fetch(`${API_BASE}/api/me`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    credentials: "include",              // <-- must be here
    body: JSON.stringify(payload),
  });

  let data;
  try {
    data = await res.json();
  } catch {
    return { error: "Failed to update profile" };
  }

  if (!res.ok) {
    return { error: data.error || "Failed to update profile" };
  }

  return data;
}