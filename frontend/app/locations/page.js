"use client";

import { useEffect, useState } from "react";
import styles from "../page.module.css";

export default function Locations() {
  const [locations, setLocations] = useState([]);
  const [searchTerm, setSearchTerm] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [cityFilter, setCityFilter] = useState("all");

  useEffect(() => {
    async function fetchLocations() {
      try {
        setLoading(true);
        const res = await fetch("http://127.0.0.1:5000/api/locations");
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const data = await res.json();
        setLocations(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : "Failed to fetch locations");
      } finally {
        setLoading(false);
      }
    }
    fetchLocations();
  }, []);

  // Get unique cities
  const cities = [...new Set(locations.map(loc => loc.city))].sort();

  const filteredLocations = locations.filter(loc => {
    const matchesSearch = 
      loc.venue_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      loc.address.toLowerCase().includes(searchTerm.toLowerCase()) ||
      loc.city.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesCity = cityFilter === "all" || loc.city === cityFilter;
    return matchesSearch && matchesCity;
  });

  return (
    <div className={styles.page}>
      {/* Hero Section */}
      <section className={styles.hero}>
        <div className={styles.heroContent}>
          <h1>Maine Venues</h1>
          <p>Discover amazing locations across Maine</p>
          <div className={styles.heroGradient}></div>
        </div>
      </section>

      {/* Search and Filter */}
      <div style={{ 
        padding: "20px", 
        display: "flex", 
        justifyContent: "center", 
        gap: "15px",
        flexWrap: "wrap",
        position: "relative",
        zIndex: 10
      }}>
        <input
          type="text"
          placeholder="Search venues..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          style={{
            padding: "12px 24px",
            width: "300px",
            borderRadius: "8px",
            border: "2px solid #9333ea",
            backgroundColor: "#1a1a2e",
            color: "white",
            fontSize: "16px",
            cursor: "text"
          }}
        />
        <select
          value={cityFilter}
          onChange={(e) => setCityFilter(e.target.value)}
          style={{
            padding: "12px 24px",
            borderRadius: "8px",
            border: "2px solid #9333ea",
            backgroundColor: "#1a1a2e",
            color: "white",
            fontSize: "16px",
            cursor: "pointer"
          }}
        >
          <option value="all">All Cities</option>
          {cities.map(city => (
            <option key={city} value={city}>{city}</option>
          ))}
        </select>
      </div>

      {/* Locations Section */}
      <main className={styles.main}>
        <div className={styles.eventsHeader}>
          <h2>{filteredLocations.length} Venues</h2>
          <div className={styles.viewAll}>View all</div>
        </div>
        
        {loading ? (
          <div className={styles.loading}>Loading venues...</div>
        ) : error ? (
          <div className={styles.error}>Error: {error}</div>
        ) : filteredLocations.length === 0 ? (
          <div className={styles.noEvents}>No venues found</div>
        ) : (
          <div className={styles.eventsGrid}>
            {filteredLocations.map((loc) => (
              <div key={loc.location_id} className={styles.eventCard}>
                <div className={styles.eventImage}>
                  <div className={styles.eventGradient}></div>
                  <div className={styles.eventTime}>{loc.zip_code}</div>
                </div>
                <div className={styles.eventContent}>
                  <div className={styles.eventMeta}>
                    <div className={styles.eventLocationIcon}>📍</div>
                    <span>{loc.city}</span>
                  </div>
                  <h3>{loc.venue_name}</h3>
                  <div className={styles.eventDate}>{loc.address}</div>
                </div>
              </div>
            ))}
          </div>
        )}
      </main>
    </div>
  );
}