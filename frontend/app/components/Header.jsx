"use client";

import { useState } from "react";
import Link from "next/link";
import styles from "../page.module.css";

const Header = ({ 
  searchTerm = "", 
  onSearchChange, 
  filter = "all", 
  onFilterChange,
  userName = "KZ"
}) => {
  const [menuOpen, setMenuOpen] = useState(false);

  return (
    <header className={styles.header}>
      <div className={styles.logo}>MaineMeetupMapper</div>
      <div className={styles.headerRight}>
        <div className={styles.searchContainer}>
          <input
            type="text"
            placeholder="Search events..."
            value={searchTerm}
            onChange={(e) => onSearchChange?.(e.target.value)}
            className={styles.searchInput}
          />
          <select 
            value={filter} 
            onChange={(e) => onFilterChange?.(e.target.value)}
            className={styles.filterSelect}
          >
            <option value="all">All</option>
            <option value="today">Today</option>
            <option value="weekend">Weekend</option>
          </select>
        </div>
        <div className={styles.userSection}>
          <div className={styles.profilePic}>{userName}</div>
          <button 
            className={styles.hamburger}
            onClick={() => setMenuOpen(!menuOpen)}
            aria-label="Toggle menu"
          >
            <span></span>
            <span></span>
            <span></span>
          </button>
          
          {/* Mobile Menu */}
          <div className={`${styles.mobileMenu} ${menuOpen ? styles.active : ""}`}>
            <div className={styles.menuHeader}>
              <div className={styles.profilePic}>{userName}</div>
              <button onClick={() => setMenuOpen(false)} aria-label="Close menu">×</button>
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
  );
};

export default Header;