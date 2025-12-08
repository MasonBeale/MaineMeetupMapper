"use client";

import { useEffect, useState } from "react";
import { apiMe, apiLogout, apiUpdateMe, apiDeleteMe } from "../lib/api";
import { useRouter } from "next/navigation";
import Header from "../components/Header";
import styles from "../page.module.css";

export default function AccountPage() {
  const router = useRouter();
  const [user, setUser] = useState(null);
  const [loadingUser, setLoadingUser] = useState(true);

  // Saved profile
  const [profile, setProfile] = useState({
    username: "",
    firstName: "",
    lastName: "",
    email: "",
  });

  // Draft form values
  const [draftFirstName, setDraftFirstName] = useState("");
  const [draftLastName, setDraftLastName] = useState("");
  const [draftEmail, setDraftEmail] = useState("");
  const [password, setPassword] = useState("");

  const [error, setError] = useState(null);
  const [message, setMessage] = useState(null);

  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false);
  const [deleting, setDeleting] = useState(false);

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
    router.push("/");  // redirect to home
  }

  function syncFromUserObject(u) {
    if (!u) return;
    const newProfile = {
      username: u.username || "",
      firstName: u.first_name || "",
      lastName: u.last_name || "",
      email: u.email || "",
    };
    setProfile(newProfile);
    setDraftFirstName(newProfile.firstName);
    setDraftLastName(newProfile.lastName);
    setDraftEmail(newProfile.email);
  }

  function handleLoggedIn(existingUser) {
    setUser(existingUser);
    syncFromUserObject(existingUser);
  }

  function handleRegistered(newUser) {
    setUser(newUser);
    syncFromUserObject(newUser);
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
      syncFromUserObject(updated);
      setPassword("");
      setMessage("Profile updated.");
    }
  }

  async function handleConfirmDelete() {
    setDeleting(true);
    setError(null);
    try {
      const res = await apiDeleteMe();
      if (res.error) {
        setError(res.error);
      } else {
        // user deleted: log out locally and optionally redirect
        setUser(null);
        setProfile({
          username: "",
          firstName: "",
          lastName: "",
          email: "",
        });
        setMessage("Your account has been deleted.");
        router.push("/");   
      }
    } catch {
      setError("Failed to delete account. Please try again.");
    } finally {
      setDeleting(false);
      setShowDeleteConfirm(false);
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

          {/* Edit form + danger zone */}
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

              {/* Danger zone */}
              <div className={styles.accountDangerZoneTitle}>
                Danger zone
              </div>
              <div className={styles.accountDangerText}>
                Deleting your account is permanent and cannot be undone. This
                will remove your profile and associated data.
              </div>
              <div className={styles.accountDangerBar}>
                <span></span>
                <button
                  type="button"
                  className={styles.deleteButton}
                  onClick={() => setShowDeleteConfirm(true)}
                >
                  Delete account
                </button>
              </div>
            </div>
          )}
        </div>
      </main>

      {showDeleteConfirm && (
        <div
          className={styles.modalOverlay}
          onClick={() => !deleting && setShowDeleteConfirm(false)}
        >
          <div
            className={styles.confirmModalContent}
            onClick={(e) => e.stopPropagation()}
          >
            <h2 className={styles.confirmTitle}>Delete account?</h2>
            <p className={styles.confirmText}>
              This action will permanently delete your account and cannot be
              undone. Are you sure you want to continue?
            </p>
            <div className={styles.confirmActions}>
              <button
                type="button"
                className={styles.confirmCancelButton}
                onClick={() => setShowDeleteConfirm(false)}
                disabled={deleting}
              >
                Cancel
              </button>
              <button
                type="button"
                className={styles.confirmDeleteButton}
                onClick={handleConfirmDelete}
                disabled={deleting}
              >
                {deleting ? "Deleting..." : "Delete account"}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
