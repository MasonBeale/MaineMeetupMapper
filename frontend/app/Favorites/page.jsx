"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import Header from "../components/Header";
import styles from "../page.module.css";
import { apiMe, apiLogout, apiGetFavorites } from "../lib/api";

export default function FavoritesPage() {
  const [user, setUser] = useState(null);
  const [favorites, setFavorites] = useState([]);
  const [loadingFavorites, setLoadingFavorites] = useState(true);
  const [error, setError] = useState(null);
  const router = useRouter();

  useEffect(() => {
    async function fetchUser() {
      const me = await apiMe();
      setUser(me);
    }
    fetchUser();
  }, []);

  useEffect(() => {
    async function fetchFavorites() {
      try {
        setLoadingFavorites(true);
        setError(null);

        const me = await apiMe();
        setUser(me);

        if (!me) {
          setFavorites([]);
          return;
        }

        const favEvents = await apiGetFavorites();
        console.log("FavoritesPage favEvents:", favEvents);
        setFavorites(Array.isArray(favEvents) ? favEvents : []);
      } catch (e) {
        setError(
          e instanceof Error ? e.message : "Failed to load favorites"
        );
      } finally {
        setLoadingFavorites(false);
      }
    }
    fetchFavorites();
  }, []);

  async function handleLogout() {
    await apiLogout();
    setUser(null);
    router.push("/");
  }

  function handleRegistered(newUser) {
    setUser(newUser);
  }

  function handleLoggedIn(existingUser) {
    setUser(existingUser);
  }

  const renderEventCard = (event) => {
    const eventId = event.id ?? event.event_id;
    const name = event.name ?? event.event_name;
    const dateStr = event.date ?? event.event_date;

    return (
      <div key={eventId} className={styles.eventCard}>
        <div className={styles.eventImage}>
          <div className={styles.eventGradient}></div>
          <div className={styles.eventTime}>
            {dateStr &&
              new Date(dateStr).toLocaleTimeString([], {
                hour: "2-digit",
                minute: "2-digit",
              })}
          </div>
        </div>
        <div className={styles.eventContent}>
          <div className={styles.eventMeta}>
            <span>
              {event.location ??
                event.location_name ??
                `Location ${event.location_id ?? ""}`}
            </span>
          </div>
          <h3>{name}</h3>
          <div className={styles.eventDate}>
            {dateStr && new Date(dateStr).toLocaleDateString()}
          </div>
          {event.description && (
            <p style={{ marginTop: "0.5rem", opacity: 0.8, fontSize: "0.9rem" }}>
              {event.description}
            </p>
          )}
        </div>
      </div>
    );
  };

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

          {loadingFavorites ? (
            <div className={styles.loading}>Loading favorites...</div>
          ) : error ? (
            <div className={styles.error}>Error: {error}</div>
          ) : favorites.length === 0 ? (
            <div className={styles.noEvents}>
              You have no favorite events yet.
            </div>
          ) : (
            <div className={styles.eventsGrid}>
              {favorites.map(renderEventCard)}
            </div>
          )}
        </section>
      </main>
    </div>
  );
}
