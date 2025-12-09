"use client";

import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import styles from "./event-detail.module.css";

export default function EventDetail() {
  const params = useParams();
  const router = useRouter();
  const [event, setEvent] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function fetchEventDetail() {
      try {
        setLoading(true);
        const res = await fetch(`http://127.0.0.1:5000/api/events/${params.id}`);
        if (!res.ok) {
          if (res.status === 404) {
            throw new Error("Event not found");
          }
          throw new Error(`HTTP ${res.status}`);
        }
        const data = await res.json();
        setEvent(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : "Failed to fetch event");
      } finally {
        setLoading(false);
      }
    }
    
    if (params.id) {
      fetchEventDetail();
    }
  }, [params.id]);

  // useEffect(() => {
  //   async function fetchRSVPs() {
  //     try {
  //       const res = await fetch("http://127.0.0.1:5000/api/analytics");
  //       if (!res.ok) throw new Error(`HTTP ${res.status}`);
  //       const data = await res.json();
  //       setAnalyticsData(data);
  //     } catch (err) {
  //       setError(err instanceof Error ? err.message : "Failed to fetch analytics");
  //     } finally {
  //       setLoading(false);
  //     }
  //   }
  //   fetchAnalytics();
  // }, []);

  const handleRSVP = () => {
    alert("RSVP functionality coming soon!");
  };

  const handleShare = () => {
    if (navigator.share) {
      navigator.share({
        title: event.name,
        text: event.description,
        url: window.location.href,
      });
    } else {
      navigator.clipboard.writeText(window.location.href);
      alert("Link copied to clipboard!");
    }
  };

  if (loading) {
    return (
      <div className={styles.page}>
        <div className={styles.loading}>Loading event details...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className={styles.page}>
        <div className={styles.error}>
          <h2>Error</h2>
          <p>{error}</p>
          <button onClick={() => router.push("/")} className={styles.backButton}>
            ← Back to Events
          </button>
        </div>
      </div>
    );
  }

  if (!event) {
    return null;
  }

  const formatDate = (dateStr) => {
    const date = new Date(dateStr);
    return date.toLocaleDateString('en-US', { 
      weekday: 'long', 
      year: 'numeric', 
      month: 'long', 
      day: 'numeric' 
    });
  };

  const formatTime = (timeStr) => {
    if (!timeStr) return '';
    const [hours, minutes] = timeStr.split(':');
    const hour = parseInt(hours);
    const ampm = hour >= 12 ? 'PM' : 'AM';
    const displayHour = hour % 12 || 12;
    return `${displayHour}:${minutes} ${ampm}`;
  };

  return (
    <div className={styles.page}>
      {/* Header */}
      <header className={styles.header}>
        <button onClick={() => router.push("/")} className={styles.backButton}>
          ← Back
        </button>
        <div className={styles.headerActions}>
          <button onClick={handleShare} className={styles.shareButton}>
            Share
          </button>
        </div>
      </header>

      {/* Hero Section */}
      <section className={styles.hero}>
        <div className={styles.heroGradient}></div>
        <div className={styles.heroContent}>
          {event.category && <div className={styles.categoryBadge}>{event.category}</div>}
          <h1>{event.name}</h1>
          <div className={styles.heroMeta}>
            <div className={styles.metaItem}>
              <span className={styles.icon}>📅</span>
              <span>{formatDate(event.date)}</span>
            </div>
            {event.time && (
              <div className={styles.metaItem}>
                <span className={styles.icon}>🕐</span>
                <span>{formatTime(event.time)}</span>
              </div>
            )}
            <div className={styles.metaItem}>
              <span className={styles.icon}>📍</span>
              <span>{event.location.city}, {event.location.state}</span>
            </div>
          </div>
        </div>
      </section>

      {/* Main Content */}
      <main className={styles.main}>
        <div className={styles.content}>
          {/* Left Column */}
          <div className={styles.leftColumn}>
            {/* Description */}
            <section className={styles.section}>
              <h2>About This Event</h2>
              <p className={styles.description}>{event.description}</p>
            </section>

            {/* Location Details */}
            <section className={styles.section}>
              <h2>Location</h2>
              <div className={styles.locationCard}>
                <h3>{event.location.name}</h3>
                <p>{event.location.address}</p>
                <p>{event.location.city}, {event.location.state} {event.location.zip_code}</p>
              </div>
            </section>

            {/* Organizer Info */}
            <section className={styles.section}>
              <h2>Organizer</h2>
              <div className={styles.organizerCard}>
                <div className={styles.organizerAvatar}>
                  {event.organizer.name.charAt(0)}
                </div>
                <div>
                  <h3>{event.organizer.name}</h3>
                  <p>{event.organizer.email}</p>
                  {event.organizer.phone && <p>{event.organizer.phone}</p>}
                </div>
              </div>
            </section>

            {/* Reviews */}
            {event.reviews && event.reviews.length > 0 && (
              <section className={styles.section}>
                <h2>Reviews ({event.reviews.length})</h2>
                <div className={styles.reviewsContainer}>
                  {event.reviews.map((review) => (
                    <div key={review.id} className={styles.reviewCard}>
                      <div className={styles.reviewHeader}>
                        <div className={styles.reviewAvatar}>
                          {review.user_name?.charAt(0) || '?'}
                        </div>
                        <div>
                          <h4>{review.user_name || 'Anonymous'}</h4>
                          <div className={styles.rating}>
                            {'⭐'.repeat(review.rating)}
                          </div>
                        </div>
                      </div>
                      {review.comment && (
                        <p className={styles.reviewComment}>{review.comment}</p>
                      )}
                    </div>
                  ))}
                </div>
              </section>
            )}
          </div>

          {/* Right Column - Sticky Card */}
          <div className={styles.rightColumn}>
            <div className={styles.stickyCard}>
              <div className={styles.priceSection}>
                {event.price > 0 ? (
                  <>
                    <div className={styles.priceLabel}>Price</div>
                    <div className={styles.price}>${event.price}</div>
                  </>
                ) : (
                  <div className={styles.freePrice}>Free Event</div>
                )}
              </div>

              <button onClick={handleRSVP} className={styles.rsvpButton}>
                RSVP to this event
              </button>

              <div className={styles.statsSection}>
                <div className={styles.stat}>
                  <div className={styles.statValue}>{event.rsvp_count}</div>
                  <div className={styles.statLabel}>Going</div>
                </div>
                <div className={styles.stat}>
                  <div className={styles.statValue}>
                    {event.avg_rating > 0 ? `⭐ ${event.avg_rating.toFixed(1)}` : 'No ratings'}
                  </div>
                  <div className={styles.statLabel}>Rating</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}