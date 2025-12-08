"use client";

import { useEffect, useState } from "react";
import { apiMe, apiLogout, apiUpdateMe } from "../lib/api";
import Header from "../components/Header";
import styles from "../page.module.css";

export default function AccountPage() {
  const [user, setUser] = useState(null);
  const [loadingUser, setLoadingUser] = useState(true);

  // Saved profile (what the server has confirmed)
  const [profile, setProfile] = useState({
    username: "",
    firstName: "",
    lastName: "",
    email: "",
  });

  // Draft values (what the user is editing)
  const [draftFirstName, setDraftFirstName] = useState("");
  const [draftLastName, setDraftLastName] = useState("");
  const [draftEmail, setDraftEmail] = useState("");
  const [password, setPassword] = useState("");

  const [error, setError] = useState(null);
  const [message, setMessage] = useState(null);

  useEffect(() => {
    async function fetchUser() {
      const me = await apiMe();
      console.log("Before PUT, apiMe says:", me);

      setUser(me);
      if (me) {
        const newProfile = {
          username: me.username || "",
          firstName: me.first_name || "",
          lastName: me.last_name || "",
          email: me.email || "",
        };
        setProfile(newProfile);

        // initialize draft from profile
        setDraftFirstName(newProfile.firstName);
        setDraftLastName(newProfile.lastName);
        setDraftEmail(newProfile.email);
      }
      setLoadingUser(false);
    }
    fetchUser();
  }, []);

  async function handleLogout() {
    await apiLogout();
    setUser(null);
  }

  function handleLoggedIn(existingUser) {
    setUser(existingUser);
    if (existingUser) {
      const newProfile = {
        username: existingUser.username || "",
        firstName: existingUser.first_name || "",
        lastName: existingUser.last_name || "",
        email: existingUser.email || "",
      };
      setProfile(newProfile);
      setDraftFirstName(newProfile.firstName);
      setDraftLastName(newProfile.lastName);
      setDraftEmail(newProfile.email);
    }
  }

  function handleRegistered(newUser) {
    setUser(newUser);
    if (newUser) {
      const newProfile = {
        username: newUser.username || "",
        firstName: newUser.first_name || "",
        lastName: newUser.last_name || "",
        email: newUser.email || "",
      };
      setProfile(newProfile);
      setDraftFirstName(newProfile.firstName);
      setDraftLastName(newProfile.lastName);
      setDraftEmail(newProfile.email);
    }
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setError(null);
    setMessage(null);

    const payload = {
      first_name: draftFirstName,
      last_name: draftLastName,
      email: draftEmail,
    };
    if (password.trim()) {
      payload.password = password.trim();
    }

    const data = await apiUpdateMe(payload);
    if (data.error) {
      setError(data.error);
    } else {
      const updated = data.user;
      setUser(updated);

      const newProfile = {
        username: updated.username || "",
        firstName: updated.first_name || "",
        lastName: updated.last_name || "",
        email: updated.email || "",
      };
      setProfile(newProfile);

      // sync draft with confirmed profile
      setDraftFirstName(newProfile.firstName);
      setDraftLastName(newProfile.lastName);
      setDraftEmail(newProfile.email);
      setPassword("");
      setMessage("Profile updated.");
    }
  }

  return (
    <div className={styles.page}>
      <Header
        searchTerm={""}
        onSearchChange={() => {}}
        filter={"all"}
        onFilterChange={() => {}}
        userName={profile.username || null}
        onLogout={handleLogout}
        onRegistered={handleRegistered}
        onLoggedIn={handleLoggedIn}
      />

      <main className={styles.main}>
        <div className={styles.accountContainer}>
          {/* Current profile summary */}
          <div className={styles.accountCard}>
            <h1 className={styles.accountTitle}>My Account</h1>

            {loadingUser ? (
              <div className={styles.loading}>Loading profile...</div>
            ) : !user ? (
              <div className={styles.error}>You are not logged in.</div>
            ) : (
              <div className={styles.accountSummaryGrid}>
                <div>
                  <div className={styles.accountSummaryLabel}>Username</div>
                  <div className={styles.accountSummaryValue}>
                    {profile.username}
                  </div>
                </div>
                <div>
                  <div className={styles.accountSummaryLabel}>Email</div>
                  <div className={styles.accountSummaryValue}>
                    {profile.email}
                  </div>
                </div>
                <div>
                  <div className={styles.accountSummaryLabel}>First name</div>
                  <div className={styles.accountSummaryValue}>
                    {profile.firstName || "—"}
                  </div>
                </div>
                <div>
                  <div className={styles.accountSummaryLabel}>Last name</div>
                  <div className={styles.accountSummaryValue}>
                    {profile.lastName || "—"}
                  </div>
                </div>
              </div>
            )}
          </div>

          {/* Edit form */}
          {user && (
            <div className={styles.accountCard}>
              {error && <div className={styles.errorMessage}>{error}</div>}

              {message && (
                <div className={styles.accountSuccessMessage}>{message}</div>
              )}

              <form onSubmit={handleSubmit}>
                <div className={styles.formGroup}>
                  <label className={styles.formLabel}>
                    Email
                    <input
                      type="email"
                      value={draftEmail}
                      onChange={(e) => setDraftEmail(e.target.value)}
                      className={styles.formInput}
                    />
                  </label>
                </div>

                <div className={styles.formGroup}>
                  <label className={styles.formLabel}>
                    First name
                    <input
                      type="text"
                      value={draftFirstName}
                      onChange={(e) => setDraftFirstName(e.target.value)}
                      className={styles.formInput}
                    />
                  </label>
                </div>

                <div className={styles.formGroup}>
                  <label className={styles.formLabel}>
                    Last name
                    <input
                      type="text"
                      value={draftLastName}
                      onChange={(e) => setDraftLastName(e.target.value)}
                      className={styles.formInput}
                    />
                  </label>
                </div>

                <div className={styles.formGroup}>
                  <label className={styles.formLabel}>
                    New password (optional)
                    <input
                      type="password"
                      value={password}
                      onChange={(e) => setPassword(e.target.value)}
                      className={styles.formInput}
                      placeholder="Leave blank to keep current password"
                    />
                  </label>
                </div>

                <button type="submit" className={styles.submitButton}>
                  Save changes
                </button>
              </form>
            </div>
          )}
        </div>
      </main>
    </div>
  );
}
