"use client";
import { useState } from "react";
import { useRouter } from "next/navigation";
import { apiRegister } from "../lib/api";
import styles from "../page.module.css";

export default function RegisterModal({ onClose, onRegistered }) {
  const router = useRouter();
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e) {
    e.preventDefault();
    setError(null);
    setLoading(true);
    
    const data = await apiRegister({ username, email, password });
    console.log("apiRegister result:", data);
    setLoading(false);
    
    if (data.error) {
      setError(data.error);
      return;
    }

    if (onRegistered && data.user) {
        onRegistered(data.user);       
      }
    
    onClose();
  }

  return (
    <div className={styles.modalOverlay} onClick={onClose}>
      <div className={styles.modalContent} onClick={(e) => e.stopPropagation()}>
        <div className={styles.modalHeader}>
          <h1 className={styles.modalTitle}>Create account</h1>
          <button className={styles.modalClose} onClick={onClose}>×</button>
        </div>
        
        {error && <div className={styles.errorMessage}>{error}</div>}
        
        <form onSubmit={handleSubmit}>
          <div className={styles.formGroup}>
            <label className={styles.formLabel}>Username</label>
            <input
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              className={styles.formInput}
              placeholder="Choose a username"
              disabled={loading}
              required
            />
          </div>
          
          <div className={styles.formGroup}>
            <label className={styles.formLabel}>Email</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className={styles.formInput}
              placeholder="your@email.com"
              disabled={loading}
              required
            />
          </div>
          
          <div className={styles.formGroup}>
            <label className={styles.formLabel}>Password</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className={styles.formInput}
              placeholder="Create a password"
              disabled={loading}
              required
              minLength="6"
            />
          </div>
          
          <button 
            type="submit" 
            className={styles.submitButton}
            disabled={loading || !username || !email || !password}
          >
            {loading ? "Creating account..." : "Sign up"}
          </button>
        </form>
      </div>
    </div>
  );
}