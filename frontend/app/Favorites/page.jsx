"use client";

import { useEffect, useState } from "react";
import Header from "../components/Header";
import styles from "../page.module.css";
import { apiMe, apiLogout } from "../lib/api";

export default function FavoritesPage() {
  const [user, setUser] = useState(null);
  const [favorites, setFavorites] = useState([]);
  const [rsvps, setRsvps] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Load current user
  useEffect(() => {
    async function fetchUser() {
      const me = await apiMe();
      setUser(me);
    }
    fetchUser();
  }, []);

  // Load favorites + RSVPs
  useEffect(() => {
    async function fetchData() {
      try {
        setLoading(true);
        setError(null);

        const [favRes, rsvpRes] = await Promise.all([
          fetch("http://127.0.0.1:5000/api/favorites", {
            credentials: "include",
          }),
          fetch("http://127.0.0.1:5000/api/rsvps", {
            credentials: "include",
          }),
        ]);

        if (!favRes.ok || !rsvpRes.ok) {
          throw new Error("Failed to load favorites or RSVPs");
        }

        const favData = await favRes.json();
        const rsvpData = await rsvpRes.json();

        setFavorites(Array.isArray(favData) ? favData : favData.events || []);
        setRsvps(Array.isArray(rsvpData) ? rsvpData : rsvpData.events || []);
      } catch (e) {
        setError(e instanceof Error ? e.message : "Failed to load data");
      } finally {
        setLoading(false);
      }
    }

    fetchData();
  }, []);

  async function handleLogout() {
    await apiLogout();
    setUser(null);
  }

  function handleRegistered(newUser) {
    setUser(newUser);
  }

  function handleLoggedIn(existingUser) {
    setUser(existingUser);
  }

  const renderEventCard = (event) => (
    <div key={event.id} className={styles.eventCard}>
      <div className={styles.eventImage}>
        <div className={styles.eventGradient}></div>
        <div className={styles.eventTime}>
          {new Date(event.date).toLocaleTimeString([], {
            hour: "2-digit",
            minute: "2-digit",
          })}
        </div>
      </div>
      <div className={styles.eventContent}>
        <div className={styles.eventMeta}>
          <div className={styles.eventLocationIcon}>📍</div>
          <span>{event.location}</span>
        </div>
        <h3>{event.name}</h3>
        <div className={styles.eventDate}>
          {new Date(event.date).toLocaleDateString()}
        </div>
      </div>
    </div>
  );

  return (
    <div className={styles.page}>
      <Header
        searchTerm={""}
        onSearchChange={() => {}}
        filter={"all"}
        onFilterChange={() => {}}
        userName={user ? user.username : null}
        onLogout={handleLogout}
        onRegistered={handleRegistered}
        onLoggedIn={handleLoggedIn}
      />

      <main className={styles.main}>
        <section className={styles.section}>
          <h2>Favorite Events</h2>

          {loading ? (
            <div className={styles.loading}>Loading favorites...</div>
          ) : error ? (
            <div className={styles.error}>Error: {error}</div>
          ) : favorites.length === 0 ? (
            <div className={styles.noEvents}>You have no favorite events yet.</div>
          ) : (
            <div className={styles.eventsGrid}>
              {favorites.map(renderEventCard)}
            </div>
          )}
        </section>

        <section className={styles.section}>
          <h2>RSVPs</h2>

          {loading ? (
            <div className={styles.loading}>Loading RSVPs...</div>
          ) : error ? (
            <div className={styles.error}>Error: {error}</div>
          ) : rsvps.length === 0 ? (
            <div className={styles.noEvents}>You have not RSVPed to any events yet.</div>
          ) : (
            <div className={styles.eventsGrid}>
              {rsvps.map(renderEventCard)}
            </div>
          )}
        </section>
      </main>
    </div>
  );
}