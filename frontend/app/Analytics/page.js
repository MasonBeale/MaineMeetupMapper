"use client";

import { useEffect, useState, useMemo, useRef, useCallback } from "react";
import { useRouter } from "next/navigation";
import Header from "../components/Header";
import styles from "../page.module.css";
import { apiMe, apiLogout } from "../lib/api";


export default function Analytics() {
  const router = useRouter();
  const [searchTerm, setSearchTerm] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [user, setUser] = useState(null);
  const [showFilters, setShowFilters] = useState(false);
  const [analyticsData, setAnalyticsData] = useState(null);


  useEffect(() => {
    async function fetchUser() {
      console.log("Calling apiMe...");
      const me = await apiMe();
      console.log("apiMe result:", me);
      setUser(me);
    }
    fetchUser();
  }, []);

  useEffect(() => {
    async function fetchAnalytics() {
      try {
        const res = await fetch("http://127.0.0.1:5000/api/analytics");
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const data = await res.json();
        setAnalyticsData(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : "Failed to fetch analytics");
      } finally {
        setLoading(false);
      }
    }
    fetchAnalytics();
  }, []);

  async function handleLogout() {
    await apiLogout();
    setUser(null);
    router.push("/"); 
  }

  function handleLoggedIn(existingUser) {
    setUser(existingUser);       
  }

  function handleRegistered(newUser) {
    setUser(newUser);
  }

  return (
    <div className={styles.page}>
      <Header 
        searchTerm={searchTerm}
        onSearchChange={setSearchTerm}
        userName={user ? user.username : null}
        onLogout={handleLogout}
        onRegistered={handleRegistered}
        onLoggedIn={handleLoggedIn}
        showFilters={showFilters}
        onShowFiltersChange={setShowFilters}
      />

      {/* Hero Section */}
      <section className={styles.hero}>
        <div className={styles.heroContent}>
          <h1>Analytics Dashboard</h1>
          <p>Track and analyze your event performance in real-time</p>
          <div className={styles.heroGradient}></div>
        </div>
      </section>

      {/* Analytics Summary Section */}
      {loading ? (
        <div className={styles.loading}>Loading analytics...</div>
      ) : error ? (
        <div className={styles.error}>Error: {error}</div>
      ) : analyticsData ? (
        <div className={styles.statsGrid}>
          <div className={styles.statCard}>
            <h3>Total Users</h3>
            <p className={styles.statNumber}>{analyticsData.totalUsers}</p>
          </div>
          
          <div className={styles.statCard}>
            <h3>Total Events</h3>
            <p className={styles.statNumber}>{analyticsData.totalEvents}</p>
          </div>
          
          <div className={styles.statCard}>
            <h3>Total Locations</h3>
            <p className={styles.statNumber}>{analyticsData.totalLocations}</p>
          </div>
        </div>
      ) : null}

    </div>
  );
}