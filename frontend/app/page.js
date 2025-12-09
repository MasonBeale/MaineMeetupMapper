"use client";

import { useEffect, useState, useMemo, useRef, useCallback } from "react";
import { useRouter } from "next/navigation";
import Header from "./components/Header";
import styles from "./page.module.css";
import { apiMe, apiLogout } from "./lib/api";


export default function Home() {
  const router = useRouter();
  const [events, setEvents] = useState([]);
  const [totalEvents, setTotalEvents] = useState(0);
  const [searchTerm, setSearchTerm] = useState("");
  const [selectedCity, setSelectedCity] = useState("all");
  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");
  const [sortBy, setSortBy] = useState("date");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [user, setUser] = useState(null);
  const [showFilters, setShowFilters] = useState(false);
  
  // Infinite scroll state
  const [displayCount, setDisplayCount] = useState(20);
  const [hasMore, setHasMore] = useState(true);
  const observerTarget = useRef(null);

  useEffect(() => {
    async function fetchUser() {
      console.log("Calling apiMe...");
      const me = await apiMe();
      console.log("apiMe result:", me);
      setUser(me);
    }
    fetchUser();
  }, []);


  // Fetch events from backend with all filters
  useEffect(() => {
    async function fetchEvents() {
      try {
        setLoading(true);
        
        // Build query parameters
        const params = new URLSearchParams();
        if (searchTerm) params.append('search', searchTerm);
        if (selectedCity !== 'all') params.append('city', selectedCity);
        if (startDate) params.append('start_date', startDate);
        if (endDate) params.append('end_date', endDate);
        params.append('sort_by', sortBy);
        params.append('limit', displayCount);
        params.append('offset', 0);
        
        const res = await fetch(`http://127.0.0.1:5000/api/events?${params}`);
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const data = await res.json();
        
        setEvents(data.events);
        setTotalEvents(data.total);
        setHasMore(data.events.length < data.total);
        setEvents(Array.isArray(data) ? data : data.events || []);
      } catch (err) {
        setError(err instanceof Error ? err.message : "Failed to fetch events");
      } finally {
        setLoading(false);
      }
    }
    fetchEvents();
  }, [searchTerm, selectedCity, startDate, endDate, sortBy, displayCount]);

  // Get unique cities from events for the dropdown
  const cities = useMemo(() => {
    const uniqueCities = [...new Set(events.map(event => event.city))].filter(Boolean);
    return uniqueCities.sort();
  }, [events]);

  // Reset display count when filters change
  useEffect(() => {
    setDisplayCount(20);
  }, [searchTerm, selectedCity, startDate, endDate, sortBy]);

  // Infinite scroll observer
  const loadMore = useCallback(() => {
    if (hasMore && !loading) {
      setDisplayCount(prev => prev + 20);
    }
  }, [hasMore, loading]);

  useEffect(() => {
    const observer = new IntersectionObserver(
      entries => {
        if (entries[0].isIntersecting) {
          loadMore();
        }
      },
      { threshold: 0.1 }
    );

    if (observerTarget.current) {
      observer.observe(observerTarget.current);
    }

    return () => {
      if (observerTarget.current) {
        observer.unobserve(observerTarget.current);
      }
    };
  }, [loadMore]);

  const handleEventClick = (eventId) => {
    router.push(`/events/${eventId}`);
  };

  const clearFilters = () => {
    setSearchTerm("");
    setSelectedCity("all");
    setStartDate("");
    setEndDate("");
    setSortBy("date");
  };

  const hasActiveFilters = searchTerm || selectedCity !== "all" || startDate || endDate || sortBy !== "date";

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
          <h1>MaineMeetupMapper</h1>
          <p>Discover amazing experiences in Maine</p>
          <div className={styles.heroGradient}></div>
        </div>
      </section>

      {/* Enhanced Search/Filter Section */}
      {showFilters && (
        <div className={styles.filterSection}>
          <div className={styles.filterContainer}>
            <div className={styles.filterRow}>
              {/* Search Input */}
              <div className={styles.filterGroup}>
                <label>Search Events</label>
                <input
                  type="text"
                  placeholder="Search by name or description..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className={styles.filterInput}
                />
              </div>

              {/* City Filter */}
              <div className={styles.filterGroup}>
                <label>City/Town</label>
                <select 
                  value={selectedCity} 
                  onChange={(e) => setSelectedCity(e.target.value)}
                  className={styles.filterSelect}
                >
                  <option value="all">All Cities</option>
                  {cities.map(city => (
                    <option key={city} value={city}>{city}</option>
                  ))}
                </select>
              </div>

              {/* Sort By */}
              <div className={styles.filterGroup}>
                <label>Sort By</label>
                <select 
                  value={sortBy} 
                  onChange={(e) => setSortBy(e.target.value)}
                  className={styles.filterSelect}
                >
                  <option value="date">Date (Earliest First)</option>
                  <option value="name">Name (A-Z)</option>
                  <option value="rating">Rating (Highest First)</option>
                  <option value="popular">Most Popular</option>
                </select>
              </div>
            </div>

            <div className={styles.filterRow}>
              {/* Start Date */}
              <div className={styles.filterGroup}>
                <label>Start Date</label>
                <input
                  type="date"
                  value={startDate}
                  onChange={(e) => setStartDate(e.target.value)}
                  className={styles.filterInput}
                />
              </div>

              {/* End Date */}
              <div className={styles.filterGroup}>
                <label>End Date</label>
                <input
                  type="date"
                  value={endDate}
                  onChange={(e) => setEndDate(e.target.value)}
                  className={styles.filterInput}
                />
              </div>

              {/* Clear Filters Button */}
              <div className={styles.filterGroup}>
                <label>&nbsp;</label>
                <button 
                  onClick={clearFilters}
                  className={styles.clearButton}
                  disabled={!hasActiveFilters}
                >
                  Clear All Filters
                </button>
              </div>
            </div>

            {/* Active Filters Display */}
            {hasActiveFilters && (
              <div className={styles.activeFilters}>
                <span className={styles.activeFiltersLabel}>Active Filters:</span>
                {searchTerm && (
                  <span className={styles.filterChip}>
                    Search: "{searchTerm}"
                    <button onClick={() => setSearchTerm("")}>×</button>
                  </span>
                )}
                {selectedCity !== "all" && (
                  <span className={styles.filterChip}>
                    City: {selectedCity}
                    <button onClick={() => setSelectedCity("all")}>×</button>
                  </span>
                )}
                {startDate && (
                  <span className={styles.filterChip}>
                    From: {new Date(startDate).toLocaleDateString()}
                    <button onClick={() => setStartDate("")}>×</button>
                  </span>
                )}
                {endDate && (
                  <span className={styles.filterChip}>
                    To: {new Date(endDate).toLocaleDateString()}
                    <button onClick={() => setEndDate("")}>×</button>
                  </span>
                )}
                {sortBy !== "date" && (
                  <span className={styles.filterChip}>
                    Sort: {sortBy === "name" ? "Name" : sortBy === "rating" ? "Rating" : "Popular"}
                    <button onClick={() => setSortBy("date")}>×</button>
                  </span>
                )}
              </div>
            )}
          </div>
        </div>
      )}

      {/* Events Section */}
      <main className={styles.main}>
        <div className={styles.eventsHeader}>
          <h2>
            {totalEvents} Event{totalEvents !== 1 ? 's' : ''}
          </h2>
          {events.length < totalEvents && (
            <div className={styles.loadingIndicator}>
              Showing {events.length} of {totalEvents}
            </div>
          )}
        </div>
        
        {loading ? (
          <div className={styles.loading}>Loading events...</div>
        ) : error ? (
          <div className={styles.error}>Error: {error}</div>
        ) : events.length === 0 ? (
          <div className={styles.noEvents}>
            <p>No events found matching your criteria</p>
            {hasActiveFilters && (
              <button onClick={clearFilters} className={styles.clearButtonLarge}>
                Clear All Filters
              </button>
            )}
          </div>
        ) : (
          <>
            <div className={styles.eventsGrid}>
              {events.map((event) => (
                <div 
                  key={event.id} 
                  className={styles.eventCard}
                  onClick={() => handleEventClick(event.id)}
                >
                  <div className={styles.eventHeader}>
                    <div className={styles.eventDateBadge}>
                      <div className={styles.dateMonth}>
                        {new Date(event.date).toLocaleDateString('en-US', { month: 'short' }).toUpperCase()}
                      </div>
                      <div className={styles.dateDay}>
                        {new Date(event.date).getDate()}
                      </div>
                    </div>
                    {event.price === 0 && (
                      <div className={styles.freeBadge}>FREE</div>
                    )}
                  </div>
                  
                  <div className={styles.eventContent}>
                    <h3>{event.name}</h3>
                    
                    <div className={styles.eventMeta}>
                      <div className={styles.metaItem}>
                        <span className={styles.icon}>🕐</span>
                        <span>{event.time ? new Date(`2000-01-01T${event.time}`).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'}) : 'TBD'}</span>
                      </div>
                      <div className={styles.metaItem}>
                        <span className={styles.icon}>📍</span>
                        <span>{event.city}, {event.state}</span>
                      </div>
                    </div>

                    {event.description && (
                      <p className={styles.eventDescription}>
                        {event.description.substring(0, 120)}
                        {event.description.length > 120 ? '...' : ''}
                      </p>
                    )}

                    <div className={styles.eventFooter}>
                      <div className={styles.eventStats}>
                        {event.avg_rating > 0 && (
                          <span className={styles.statItem}>
                            ⭐ {event.avg_rating.toFixed(1)}
                          </span>
                        )}
                        <span className={styles.statItem}>
                          👥 {event.rsvp_count} going
                        </span>
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>

            {/* Infinite scroll trigger */}
            {hasMore && (
              <div ref={observerTarget} className={styles.loadMoreTrigger}>
                <div className={styles.loadingSpinner}>Loading more events...</div>
              </div>
            )}

            {!hasMore && events.length > 20 && (
              <div className={styles.endMessage}>
                You've reached the end! 🎉
              </div>
            )}
          </>
        )}
      </main>
    </div>
  );
}