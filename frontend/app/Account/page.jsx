"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { apiMe, apiUpdateMe } from "../lib/api";

export default function AccountPage() {
  const router = useRouter();
  const [loading, setLoading] = useState(true);
  const [email, setEmail] = useState("");
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [error, setError] = useState(null);
  const [message, setMessage] = useState(null);

  useEffect(() => {
    async function loadUser() {
      const me = await apiMe();
      if (!me || me.error) {
        router.push("/login");
        return;
      }
      setEmail(me.email || "");
      setFirstName(me.first_name || "");
      setLastName(me.last_name || "");
      setLoading(false);
    }
    loadUser();
  }, [router]);

  async function handleSubmit(e) {
    e.preventDefault();
    setError(null);
    setMessage(null);
    const data = await apiUpdateMe({
      email,
      first_name: firstName,
      last_name: lastName,
    });
    if (data.error) {
      setError(data.error);
    } else {
      setMessage("Profile updated.");
    }
  }

  if (loading) {
    return <div style={{ padding: "24px" }}>Loading...</div>;
  }

  return (
    <div style={{ padding: "24px" }}>
      <h1>Account</h1>
      {error && <div style={{ color: "red" }}>{error}</div>}
      {message && <div style={{ color: "green" }}>{message}</div>}
      <form onSubmit={handleSubmit}>
        <div style={{ marginBottom: "8px" }}>
          <label>
            Email
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              style={{ display: "block", width: "100%", marginTop: "4px" }}
            />
          </label>
        </div>
        <div style={{ marginBottom: "8px" }}>
          <label>
            First name
            <input
              type="text"
              value={firstName}
              onChange={(e) => setFirstName(e.target.value)}
              style={{ display: "block", width: "100%", marginTop: "4px" }}
            />
          </label>
        </div>
        <div style={{ marginBottom: "8px" }}>
          <label>
            Last name
            <input
              type="text"
              value={lastName}
              onChange={(e) => setLastName(e.target.value)}
              style={{ display: "block", width: "100%", marginTop: "4px" }}
            />
          </label>
        </div>
        <button type="submit">Save changes</button>
      </form>
    </div>
  );
}