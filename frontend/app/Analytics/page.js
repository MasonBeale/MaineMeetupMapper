"use client";

import { useEffect, useState } from "react";
import styles from "../page.module.css";

export default function Analytics() {
  const [analyticsData, setAnalyticsData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [timeRange, setTimeRange] = useState("month"); // day, week, month, year

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
    return <div className={styles.loading}>Loading analytics...</div>;
  }

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <h1>Analytics Dashboard</h1>
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
      </div>

      {/* Summary Cards */}
      <div className={styles.summaryGrid}>
        <div className={styles.summaryCard}>
          <h3>Total Events</h3>
          <div className={styles.value}>{analyticsData?.totalEvents || 0}</div>
          <div className={styles.change}>+12% from last {timeRange}</div>
        </div>
        
        <div className={styles.summaryCard}>
          <h3>Active Users</h3>
          <div className={styles.value}>{analyticsData?.activeUsers || 0}</div>
          <div className={styles.change}>+8% from last {timeRange}</div>
        </div>
        
        <div className={styles.summaryCard}>
          <h3>Popular Locations</h3>
          <div className={styles.value}>{analyticsData?.popularLocations?.length || 0}</div>
          <div className={styles.change}>Top: {analyticsData?.popularLocations?.[0] || "N/A"}</div>
        </div>
        
        <div className={styles.summaryCard}>
          <h3>Avg. Attendance</h3>
          <div className={styles.value}>{analyticsData?.avgAttendance || 0}</div>
          <div className={styles.change}>+5% from last {timeRange}</div>
        </div>
      </div>

      {/* Charts Section */}
      <div className={styles.chartsGrid}>
        <div className={styles.chartCard}>
          <h3>Events Over Time</h3>
          {/* Chart placeholder */}
          <div className={styles.chartPlaceholder}>
            <div className={styles.bar} style={{ height: "70%" }}></div>
            <div className={styles.bar} style={{ height: "90%" }}></div>
            <div className={styles.bar} style={{ height: "60%" }}></div>
            <div className={styles.bar} style={{ height: "85%" }}></div>
            <div className={styles.bar} style={{ height: "75%" }}></div>
          </div>
        </div>
        
        <div className={styles.chartCard}>
          <h3>User Engagement</h3>
          {/* Chart placeholder */}
          <div className={styles.chartPlaceholder}>
            <div className={styles.line}></div>
          </div>
        </div>
      </div>

      {/* Detailed Statistics */}
      <div className={styles.detailedStats}>
        <div className={styles.statSection}>
          <h3>Top Event Categories</h3>
          <ul className={styles.categoryList}>
            {analyticsData?.topCategories?.map((category, index) => (
              <li key={index} className={styles.categoryItem}>
                <span className={styles.categoryName}>{category.name}</span>
                <span className={styles.categoryCount}>{category.count} events</span>
              </li>
            ))}
          </ul>
        </div>
        
        <div className={styles.statSection}>
          <h3>Recent Activity</h3>
          <ul className={styles.activityList}>
            {analyticsData?.recentActivity?.map((activity, index) => (
              <li key={index} className={styles.activityItem}>
                <div className={styles.activityIcon}>📅</div>
                <div className={styles.activityContent}>
                  <div className={styles.activityText}>{activity.text}</div>
                  <div className={styles.activityTime}>{activity.time}</div>
                </div>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
}
