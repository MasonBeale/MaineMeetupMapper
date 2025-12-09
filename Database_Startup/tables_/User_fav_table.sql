-- Author: Kristina Zbinden using Perplexity AI
-- Schema for User favorite Table

CREATE TABLE IF NOT EXISTS UserFavoriteEvent (
  user_id  INT NOT NULL,
  event_id INT NOT NULL,
  favorited_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (user_id, event_id),
  FOREIGN KEY (user_id)  REFERENCES User(user_id)  ON DELETE CASCADE,
  FOREIGN KEY (event_id) REFERENCES Event(event_id) ON DELETE CASCADE
);