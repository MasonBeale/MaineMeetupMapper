"use client";

import { useEffect, useState } from "react";
import Image from "next/image";
import Link from "next/link";
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
      {/* Header */}
      <header className={styles.header}>
        <div className={styles.logo}>MaineMeetupMapper</div>
        <div className={styles.headerRight}>
          <div className={styles.searchContainer}>
            <input
              type="text"
              placeholder="Search events..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className={styles.searchInput}
            />
            <select 
              value={filter} 
              onChange={(e) => setFilter(e.target.value)}
              className={styles.filterSelect}
            >
              <option value="all">All</option>
              <option value="today">Today</option>
              <option value="weekend">Weekend</option>
            </select>
            </div>
            <div className={styles.userSection}>
              <div className={styles.profilePic}>KZ</div>
              <button 
                className={styles.hamburger}
                onClick={() => setMenuOpen(!menuOpen)}
              >
                <span></span>
                <span></span>
                <span></span>
              </button>
              {/* Mobile Menu */}
              <div className={`${styles.mobileMenu} ${menuOpen ? styles.active : ""}`}>
                <div className={styles.menuHeader}>
                  <div className={styles.profilePic}>KZ</div>
                  <button onClick={() => setMenuOpen(false)}>×</button>
                </div>
                <nav className={styles.menuNav}>
                  <Link href="/" onClick={() => setMenuOpen(false)}>Home</Link>
                  <Link href="/Analytics" className={styles.navLink}>Analytics</Link>
                  <a href="/profile" onClick={() => setMenuOpen(false)}>Profile</a>
                  <a href="/favorites" onClick={() => setMenuOpen(false)}>Favorites</a>
                  <a href="/settings" onClick={() => setMenuOpen(false)}>Settings</a>
                  <a href="/login" onClick={() => setMenuOpen(false)}>Logout</a>
                </nav>
              </div>
              {/* Overlay */}
              {menuOpen && (
                <div 
                  className={styles.menuOverlay}
                  onClick={() => setMenuOpen(false)}
                />
              )}
            </div>
        </div>
      </header>

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
