"use client";

import { useEffect, useState } from "react";
import Header from "./components/Header";
import styles from "./page.module.css";
import {
  apiMe,
  apiLogout,
  apiGetFavorites,
  apiFavorite,
  apiUnfavorite,
} from "./lib/api";
import { useRouter } from "next/navigation";

export default function Home() {
  const [events, setEvents] = useState([]);
  const [searchTerm, setSearchTerm] = useState("");
  const [favorites, setFavorites] = useState([]); // array of event_ids
  const [filter, setFilter] = useState("all");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [user, setUser] = useState(null);
  const router = useRouter();

  // Load user once
  useEffect(() => {
    async function fetchUser() {
      const me = await apiMe();
      setUser(me);
    }
    fetchUser();
  }, []);

  // Load user + favorites (event_id list)
  useEffect(() => {
    async function fetchUserAndFavorites() {
      const me = await apiMe();
      setUser(me);
      if (me) {
        const favEvents = await apiGetFavorites();
        // backend should return [{ event_id, ... }]
        setFavorites(favEvents.map((e) => e.event_id));
      } else {
        setFavorites([]);
      }
    }
    fetchUserAndFavorites();
  }, []);

  // Load events from backend
  useEffect(() => {
    async function fetchEvents() {
      try {
        setLoading(true);
        const res = await fetch("http://127.0.0.1:5000/api/events");
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const data = await res.json();
        // normalize shape: events array
        const list = Array.isArray(data) ? data : data.events || [];
        setEvents(list);
      } catch (err) {
        setError(
          err instanceof Error ? err.message : "Failed to fetch events"
        );
      } finally {
        setLoading(false);
      }
    }
    fetchEvents();
  }, []);

  async function handleToggleFavorite(eventId) {
    if (!user) return; // optionally open login modal
    const isFav = favorites.includes(eventId);
    if (isFav) {
      await apiUnfavorite(eventId);
      setFavorites((prev) => prev.filter((id) => id !== eventId));
    } else {
      await apiFavorite(eventId);
      setFavorites((prev) => [...prev, eventId]);
    }
  }

  const filteredEvents = events.filter((event) => {
    // match backend field names: event_name, event_date
    const name = event.name ?? event.event_name ?? "";
    const dateStr = event.date ?? event.event_date;

    const matchesSearch = name
      .toLowerCase()
      .includes(searchTerm.toLowerCase());

    const eventDate = dateStr ? new Date(dateStr) : null;
    const today = new Date();

    const isToday =
      eventDate &&
      eventDate.toDateString() === today.toDateString();

    const isWeekend =
      eventDate && [0, 6].includes(eventDate.getDay());

    const matchesFilter =
      filter === "all" ||
      (filter === "today" && isToday) ||
      (filter === "weekend" && isWeekend);

    return matchesSearch && matchesFilter;
  });

  function handleRegistered(newUser) {
    setUser(newUser);
  }

  async function handleLogout() {
    await apiLogout();
    setUser(null);
    router.push("/");
  }

  function handleLoggedIn(existingUser) {
    setUser(existingUser);
  }

  return (
    <div className={styles.page}>
      <Header
        searchTerm={searchTerm}
        onSearchChange={setSearchTerm}
        filter={filter}
        onFilterChange={setFilter}
        userName={user ? user.username : null}
        onLogout={handleLogout}
        onRegistered={handleRegistered}
        onLoggedIn={handleLoggedIn}
      />

      {/* Hero Section */}
      <section className={styles.hero}>
        <div className={styles.heroContent}>
          <h1>MaineMeetupMapper</h1>
          <p>Discover amazing experiences in Maine</p>
          <div className={styles.heroGradient}></div>
        </div>
      </section>

      {/* Events Section */}
      <main className={styles.main}>
        <div className={styles.eventsHeader}>
          <h2>{filteredEvents.length} Events</h2>
          <div className={styles.viewAll}>View all</div>
        </div>

        {loading ? (
          <div className={styles.loading}>Loading events...</div>
        ) : error ? (
          <div className={styles.error}>Error: {error}</div>
        ) : filteredEvents.length === 0 ? (
          <div className={styles.noEvents}>No events found</div>
        ) : (
          <div className={styles.eventsGrid}>
            {filteredEvents.map((event) => {
              const eventId = event.event_id ?? event.id;
              const name = event.name ?? event.event_name;
              const dateStr = event.date ?? event.event_date;
              const isFav = favorites.includes(eventId);

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
                      <div className={styles.eventLocationIcon}>📍</div>
                      <span>
                        {event.location ??
                          event.location_name ??
                          `Location ${event.location_id ?? ""}`}
                      </span>
                    </div>
                    <h3>{name}</h3>
                    <div className={styles.eventDate}>
                      {dateStr &&
                        new Date(dateStr).toLocaleDateString()}
                    </div>

                    <button
                      type="button"
                      className={styles.menuButton}
                      onClick={() => handleToggleFavorite(eventId)}
                    >
                      {isFav ? "★ Favorited" : "☆ Favorite"}
                    </button>
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </main>
    </div>
  );
}
