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
    
    let data = null;
    try {
      data = await res.json();
    } catch (e) {
      // backend returned HTML error; surface a generic error
      return { error: "Login failed (non-JSON response)" };
    }
  
    if (!res.ok) {
      return { error: data.error || "Login failed" };
    }
  
    return data; // { user: {...} }
  }

  export async function apiLogout() {
    const res = await fetch(`${API_BASE}/api/logout`, {
      method: "POST",
      credentials: "include",            
    });
    return res.json();
  }

export async function apiMe() {
    const res = await fetch(`${API_BASE}/api/me`, {
      method: "GET",
      credentials: "include",
    });
    if (!res.ok) return None;
    const data = await res.json();
    return data.user; 
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