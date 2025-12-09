-- Author: Kristina Zbinden using Perplexity AI
-- Schema for User Table

CREATE TABLE IF NOT EXISTS User (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_created_at (created_at),
    INDEX idx_updated_at (updated_at)
);

CREATE TABLE IF NOT EXISTS UserFavoriteEvent (
  user_id  INT NOT NULL,
  event_id INT NOT NULL,
  favorited_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (user_id, event_id),
  FOREIGN KEY (user_id)  REFERENCES User(user_id)  ON DELETE CASCADE,
  FOREIGN KEY (event_id) REFERENCES Event(event_id) ON DELETE CASCADE
);