"use client";

import { useState } from "react";
import Link from "next/link";
import styles from "../page.module.css";
import LoginModal from "./LoginModal";
import RegisterModal from "./RegisterModal";

const Header = ({ 
  searchTerm = "", 
  onSearchChange, 
  filter = "all", 
  onFilterChange,
  userName = null,          
  onLogout, 
  onRegistered,
  onLoggedIn,           
}) => {
  const [menuOpen, setMenuOpen] = useState(false);

  // Derive initials from userName 
  const initials = userName
  ? userName
      .split(" ")
      .map((part) => part[0])
      .join("")
      .toUpperCase()
  : "";

  const [showLoginModal, setShowLoginModal] = useState(false);
  const [showRegisterModal, setShowRegisterModal] = useState(false);

  const isLoggedIn = !!userName;


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
          {/* Header circle: initials if logged in, generic if not */}
          <div className={styles.profilePic}>
            {isLoggedIn ? initials : "?"}
          </div>

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
              <div className={styles.profilePic}>
                {isLoggedIn ? initials : "?"}
              </div>
              <button
                onClick={() => setMenuOpen(false)}
                aria-label="Close menu"
              >
                ×
              </button>
            </div>
            <nav className={styles.menuNav}>
              <Link href="/" onClick={() => setMenuOpen(false)}>Home</Link>
              <Link href="/Analytics" className={styles.navLink}>Analytics</Link>
              {isLoggedIn ? (
                <>
                  <Link href="/Account" className={styles.navLink}>My Account</Link>
                  <Link href="/Favorites" className={styles.navLink}>Favorites & RSVPs</Link>
                  <button
                    type="button"
                    onClick={async () => {
                      // Call logout handler if provided
                      if (onLogout) {
                        await onLogout();
                      }
                      setMenuOpen(false);
                    }}
                    className={styles.menuButton}
                  >
                    Log out
                  </button>
                </>
              ) : (
                <> 
                  <button onClick={() => setShowLoginModal(true)} className={styles.menuButton}>Log in</button>
                  <button onClick={() => setShowRegisterModal(true)} className={styles.menuButton}>Sign up</button>
                </>
              )}
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
      {showLoginModal && (
        <LoginModal onClose={() => setShowLoginModal(false)} 
        onLoggedIn={onLoggedIn} />
      )}
      {showRegisterModal && (
        <RegisterModal onClose={() => setShowRegisterModal(false)}
        onRegistered={onRegistered}  />
      )}
    </header>
  );
};

export default Header;