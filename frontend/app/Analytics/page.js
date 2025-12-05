"use client";

import { useEffect, useState } from "react";
import styles from "../page.module.css";

export default function Analytics() {
  const [analyticsData, setAnalyticsData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [timeRange, setTimeRange] = useState("month"); // day, week, month, year
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  useEffect(() => {
    fetchAnalyticsData();
  }, [timeRange]);

  async function fetchAnalyticsData() {
    try {
      setLoading(true);
      const res = await fetch(
        `http://127.0.0.1:5000/api/analytics?range=${timeRange}`
      );
      const data = await res.json();
      setAnalyticsData(data);
    } catch (error) {
      console.error("Failed to fetch analytics:", error);
    } finally {
      setLoading(false);
    }
  }

  if (loading) {
    return (
      <div className={styles.page}>
        <div className={styles.loading}>Loading analytics...</div>
      </div>
    );
  }

  return (
    <div className={styles.page}>
      {/* Header */}
      <header className={styles.header}>
        <div className={styles.logo}>Analytics</div>
        
        <div className={styles.headerRight}>
          <div className={styles.searchContainer}>
            <div className={styles.searchIcon}>🔍</div>
            <input 
              type="text" 
              className={styles.searchInput}
              placeholder="Search analytics..."
            />
          </div>
          
          <select className={styles.filterSelect} value={timeRange} onChange={(e) => setTimeRange(e.target.value)}>
            <option value="day">Day</option>
            <option value="week">Week</option>
            <option value="month">Month</option>
            <option value="year">Year</option>
          </select>
          
          <div className={styles.userSection}>
            <div className={styles.profilePic}>JD</div>
            <button 
              className={styles.hamburger} 
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            >
              <span></span>
              <span></span>
              <span></span>
            </button>
          </div>
        </div>
      </header>

      {/* Mobile Menu */}
      <div className={`${styles.mobileMenu} ${mobileMenuOpen ? styles.active : ""}`}>
        <div className={styles.menuHeader}>
          <h3>Menu</h3>
          <button onClick={() => setMobileMenuOpen(false)}>✕</button>
        </div>
        <nav className={styles.menuNav}>
          <a href="#">Dashboard</a>
          <a href="#">Events</a>
          <a href="#">Analytics</a>
          <a href="#">Users</a>
          <a href="#">Settings</a>
        </nav>
      </div>

      {/* Hero Section */}
      <section className={styles.hero}>
        <div className={styles.heroGradient}></div>
        <div className={styles.heroContent}>
          <h1>Analytics Dashboard</h1>
          <p>Track and analyze your event performance in real-time</p>
        </div>
      </section>

      {/* Main Content */}
      <main className={styles.main}>
        {/* Summary Cards */}
        <div className={styles.eventsHeader}>
          <h2>Overview</h2>
          <div className={styles.viewAll}>View Details →</div>
        </div>
        
        <div className={styles.eventsGrid}>
          {/* Total Events Card */}
          <div className={styles.eventCard}>
            <div className={styles.eventImage}>
              <div className={styles.eventGradient}></div>
              <div className={styles.eventTime}>📊</div>
            </div>
            <div className={styles.eventContent}>
              <div className={styles.eventMeta}>
                <span className={styles.eventLocationIcon}>📈</span>
                <span>Total Events</span>
              </div>
              <h3>{analyticsData?.totalEvents || 0}</h3>
              <div className={styles.eventDate}>+12% from last {timeRange}</div>
            </div>
          </div>
          
          {/* Active Users Card */}
          <div className={styles.eventCard}>
            <div className={styles.eventImage}>
              <div className={styles.eventGradient}></div>
              <div className={styles.eventTime}>👥</div>
            </div>
            <div className={styles.eventContent}>
              <div className={styles.eventMeta}>
                <span className={styles.eventLocationIcon}>🔥</span>
                <span>Active Users</span>
              </div>
              <h3>{analyticsData?.activeUsers || 0}</h3>
              <div className={styles.eventDate}>+8% from last {timeRange}</div>
            </div>
          </div>
          
          {/* Popular Locations Card */}
          <div className={styles.eventCard}>
            <div className={styles.eventImage}>
              <div className={styles.eventGradient}></div>
              <div className={styles.eventTime}>📍</div>
            </div>
            <div className={styles.eventContent}>
              <div className={styles.eventMeta}>
                <span className={styles.eventLocationIcon}>🏆</span>
                <span>Popular Locations</span>
              </div>
              <h3>{analyticsData?.popularLocations?.length || 0}</h3>
              <div className={styles.eventDate}>
                Top: {analyticsData?.popularLocations?.[0] || "N/A"}
              </div>
            </div>
          </div>
          
          {/* Avg Attendance Card */}
          <div className={styles.eventCard}>
            <div className={styles.eventImage}>
              <div className={styles.eventGradient}></div>
              <div className={styles.eventTime}>📊</div>
            </div>
            <div className={styles.eventContent}>
              <div className={styles.eventMeta}>
                <span className={styles.eventLocationIcon}>👤</span>
                <span>Avg. Attendance</span>
              </div>
              <h3>{analyticsData?.avgAttendance || 0}</h3>
              <div className={styles.eventDate}>+5% from last {timeRange}</div>
            </div>
          </div>
        </div>

        {/* Charts Section */}
        <div className={styles.eventsHeader} style={{ marginTop: "4rem" }}>
          <h2>Charts & Trends</h2>
          <div className={styles.viewAll}>Export Data →</div>
        </div>
        
        <div className={styles.eventsGrid}>
          {/* Events Over Time */}
          <div className={styles.eventCard}>
            <div className={styles.eventImage} style={{ height: "150px" }}>
              <div className={styles.eventGradient}></div>
            </div>
            <div className={styles.eventContent}>
              <h3>Events Over Time</h3>
              <div className={styles.eventDate}>
                {timeRange === "day" ? "Daily" : 
                 timeRange === "week" ? "Weekly" : 
                 timeRange === "month" ? "Monthly" : "Yearly"} trends
              </div>
            </div>
          </div>
          
          {/* User Engagement */}
          <div className={styles.eventCard}>
            <div className={styles.eventImage} style={{ height: "150px" }}>
              <div className={styles.eventGradient}></div>
            </div>
            <div className={styles.eventContent}>
              <h3>User Engagement</h3>
              <div className={styles.eventDate}>Session duration and interactions</div>
            </div>
          </div>
        </div>

        {/* Detailed Statistics */}
        <div className={styles.eventsHeader} style={{ marginTop: "4rem" }}>
          <h2>Detailed Analytics</h2>
          <div className={styles.viewAll}>See All →</div>
        </div>
        
        <div className={styles.eventsGrid}>
          {/* Top Categories */}
          <div className={styles.eventCard}>
            <div className={styles.eventContent}>
              <h3>Top Event Categories</h3>
              <ul style={{ marginTop: "1rem", padding: 0, listStyle: "none" }}>
                {analyticsData?.topCategories?.map((category, index) => (
                  <li key={index} style={{ 
                    display: "flex", 
                    justifyContent: "space-between", 
                    padding: "0.75rem 0",
                    borderBottom: "1px solid rgba(255,255,255,0.05)"
                  }}>
                    <span>{category.name}</span>
                    <span style={{ color: "#a855f7", fontWeight: "600" }}>
                      {category.count} events
                    </span>
                  </li>
                )) || (
                  <li style={{ padding: "0.75rem 0", opacity: 0.7 }}>
                    No category data available
                  </li>
                )}
              </ul>
            </div>
          </div>
          
          {/* Recent Activity */}
          <div className={styles.eventCard}>
            <div className={styles.eventContent}>
              <h3>Recent Activity</h3>
              <ul style={{ marginTop: "1rem", padding: 0, listStyle: "none" }}>
                {analyticsData?.recentActivity?.map((activity, index) => (
                  <li key={index} style={{ 
                    display: "flex", 
                    alignItems: "center",
                    gap: "1rem",
                    padding: "0.75rem 0",
                    borderBottom: "1px solid rgba(255,255,255,0.05)"
                  }}>
                    <div style={{ 
                      width: "32px", 
                      height: "32px", 
                      borderRadius: "50%", 
                      background: "rgba(168, 85, 247, 0.2)",
                      display: "flex",
                      alignItems: "center",
                      justifyContent: "center"
                    }}>
                      📅
                    </div>
                    <div style={{ flex: 1 }}>
                      <div style={{ fontSize: "0.9rem" }}>{activity.text}</div>
                      <div style={{ fontSize: "0.8rem", opacity: 0.7 }}>{activity.time}</div>
                    </div>
                  </li>
                )) || (
                  <li style={{ padding: "0.75rem 0", opacity: 0.7 }}>
                    No recent activity
                  </li>
                )}
              </ul>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}