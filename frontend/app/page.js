"use client";

import { useEffect, useState } from "react";
import Image from "next/image";
import Link from "next/link";
import Header from "./components/Header";
import styles from "./page.module.css";

export default function Home() {
  const [events, setEvents] = useState([]);
  const [searchTerm, setSearchTerm] = useState("");
  const [filter, setFilter] = useState("all");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [menuOpen, setMenuOpen] = useState(false);

  useEffect(() => {
    async function fetchEvents() {
      try {
        setLoading(true);
        const res = await fetch("http://127.0.0.1:5000/api/events");
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const data = await res.json();
        setEvents(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : "Failed to fetch events");
      } finally {
        setLoading(false);
      }
    }
    fetchEvents();
  }, []);

  const filteredEvents = events.filter(event => {
    const matchesSearch = event.name.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesFilter = filter === "all" || 
      (filter === "today" && new Date(event.date).toDateString() === new Date().toDateString()) ||
      (filter === "weekend" && [0,6].includes(new Date(event.date).getDay()));
    return matchesSearch && matchesFilter;
  });

  return (
    <div className={styles.page}>
      <Header 
        searchTerm={searchTerm}
        onSearchChange={setSearchTerm}
        filter={filter}
        onFilterChange={setFilter}
        userName="KZ"
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
            {filteredEvents.map((event, index) => (
              <div key={event.id} className={styles.eventCard}>
                <div className={styles.eventImage}>
                  <div className={styles.eventGradient}></div>
                  <div className={styles.eventTime}>{new Date(event.date).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}</div>
                </div>
                <div className={styles.eventContent}>
                  <div className={styles.eventMeta}>
                    <div className={styles.eventLocationIcon}>📍</div>
                    <span>{event.location}</span>
                  </div>
                  <h3>{event.name}</h3>
                  <div className={styles.eventDate}>{new Date(event.date).toLocaleDateString()}</div>
                </div>
              </div>
            ))}
          </div>
        )}
      </main>
    </div>
  );
}
