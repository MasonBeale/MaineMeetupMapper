"use client";

import { useEffect, useState } from "react";
import styles from "../page.module.css";
import Header from "../components/Header";

export default function Analytics() {
  const [analyticsData, setAnalyticsData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [timeRange, setTimeRange] = useState("month");
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [searchTerm, setSearchTerm] = useState("");
  const [filter, setFilter] = useState("all");

  // Add time range selector component
  const TimeRangeSelector = () => (
    <div className={styles.timeRangeSelector}>
      <button 
        className={timeRange === "day" ? styles.active : ""} 
        onClick={() => setTimeRange("day")}
      >
        Day
      </button>
      <button 
        className={timeRange === "week" ? styles.active : ""} 
        onClick={() => setTimeRange("week")}
      >
        Week
      </button>
      <button 
        className={timeRange === "month" ? styles.active : ""} 
        onClick={() => setTimeRange("month")}
      >
        Month
      </button>
      <button 
        className={timeRange === "year" ? styles.active : ""} 
        onClick={() => setTimeRange("year")}
      >
        Year
      </button>
    </div>
  );

  useEffect(() => {
    fetchAnalyticsData();
  }, [timeRange]);

  async function fetchAnalyticsData() {
    try {
      setLoading(true);
      setError(null);
      
      // Try to fetch from Flask backend
      const res = await fetch(
        `http://localhost:5000/api/analytics?range=${timeRange}`,
        {
          method: 'GET',
          headers: {
            'Accept': 'application/json',
          }
        }
      );
      
      if (!res.ok) {
        throw new Error(`HTTP error! Status: ${res.status}`);
      }
      
      const data = await res.json();
      setAnalyticsData(data);
    } catch (error) {
      console.error("Failed to fetch analytics:", error);
      setError("Failed to load analytics data. Please check if the Flask server is running.");
      
      // Fallback mock data for development
      setAnalyticsData({
        totalEvents: 24,
        activeUsers: 156,
        avgAttendance: 42,
        popularLocations: ["Downtown", "Campus", "Westside", "East End"],
        topCategories: [
          {name: "Music & Concerts", count: 12},
          {name: "Workshops", count: 8},
          {name: "Sports", count: 6},
          {name: "Food & Drink", count: 4}
        ],
        recentActivity: [
          {text: "System running in fallback mode", time: "Just now"},
          {text: "Flask backend not connected", time: "5 min ago"},
          {text: "Using mock data for display", time: "10 min ago"}
        ]
      });
    } finally {
      setLoading(false);
    }
  }

  // Add CSS for time range selector
  const timeRangeStyles = `
    .timeRangeSelector {
      display: flex;
      gap: 0.5rem;
      margin: 1rem 0;
      justify-content: center;
    }
    
    .timeRangeSelector button {
      padding: 0.5rem 1rem;
      background: rgba(255, 255, 255, 0.1);
      border: 1px solid rgba(255, 255, 255, 0.2);
      border-radius: 6px;
      color: white;
      cursor: pointer;
      transition: all 0.3s ease;
      font-family: inherit;
    }
    
    .timeRangeSelector button:hover {
      background: rgba(255, 255, 255, 0.2);
    }
    
    .timeRangeSelector button.active {
      background: #a855f7;
      border-color: #a855f7;
    }
  `;

  if (loading) {
    return (
      <div className={styles.page}>
        <style>{timeRangeStyles}</style>
        <div className={styles.loading}>Loading analytics...</div>
      </div>
    );
  }

  // Render the main content
  return (
    <div className={styles.page}>
      <style>{timeRangeStyles}</style>
      
      {/* Header */}
      <Header 
        searchTerm={searchTerm}
        onSearchChange={setSearchTerm}
        filter={filter}
        onFilterChange={setFilter}
        userName="KZ"
      />

      {/* Hero Section */}
      <section className={styles.hero}>
        <div className={styles.heroGradient}></div>
        <div className={styles.heroContent}>
          <h1>Analytics Dashboard</h1>
          <p>Track and analyze your event performance in real-time</p>
          
          {/* Time Range Selector */}
          <TimeRangeSelector />
          
          {/* Error Message */}
          {error && (
            <div className={styles.errorMessage}>
              ⚠️ {error} - Using fallback data
            </div>
          )}
        </div>
      </section>

      {/* Stats Grid */}
      {analyticsData && (
        <div className={styles.statsGrid}>
          <div className={styles.statCard}>
            <h3>Total Events</h3>
            <p className={styles.statNumber}>{analyticsData.totalEvents}</p>
            <span className={styles.statChange}>+12% from last {timeRange}</span>
          </div>
          
          <div className={styles.statCard}>
            <h3>Active Users</h3>
            <p className={styles.statNumber}>{analyticsData.activeUsers}</p>
            <span className={styles.statChange}>+8% from last {timeRange}</span>
          </div>
          
          <div className={styles.statCard}>
            <h3>Avg. Attendance</h3>
            <p className={styles.statNumber}>{analyticsData.avgAttendance}</p>
            <span className={styles.statChange}>+5% from last {timeRange}</span>
          </div>
        </div>
      )}

      {/* Popular Locations */}
      {analyticsData && analyticsData.popularLocations && (
        <section className={styles.section}>
          <h2>Popular Locations</h2>
          <div className={styles.locationsGrid}>
            {analyticsData.popularLocations.map((location, index) => (
              <div key={index} className={styles.locationCard}>
                <div className={styles.locationIcon}>📍</div>
                <h4>{location}</h4>
                <p>{Math.floor(Math.random() * 50) + 20} events this {timeRange}</p>
              </div>
            ))}
          </div>
        </section>
      )}

      {/* Top Categories */}
      {analyticsData && analyticsData.topCategories && (
        <section className={styles.section}>
          <h2>Top Categories</h2>
          <div className={styles.categoriesList}>
            {analyticsData.topCategories.map((category, index) => (
              <div key={index} className={styles.categoryItem}>
                <div className={styles.categoryInfo}>
                  <h4>{category.name}</h4>
                  <span>{category.count} events</span>
                </div>
                <div className={styles.categoryBar}>
                  <div 
                    className={styles.categoryBarFill}
                    style={{ width: `${(category.count / analyticsData.totalEvents) * 100}%` }}
                  ></div>
                </div>
              </div>
            ))}
          </div>
        </section>
      )}

      {/* Recent Activity */}
      {analyticsData && analyticsData.recentActivity && (
        <section className={styles.section}>
          <h2>Recent Activity</h2>
          <div className={styles.activityList}>
            {analyticsData.recentActivity.map((activity, index) => (
              <div key={index} className={styles.activityItem}>
                <div className={styles.activityDot}></div>
                <div className={styles.activityContent}>
                  <p>{activity.text}</p>
                  <span className={styles.activityTime}>{activity.time}</span>
                </div>
              </div>
            ))}
          </div>
        </section>
      )}
    </div>
  );
}