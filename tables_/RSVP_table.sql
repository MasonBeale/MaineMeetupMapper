-- just making the RSVP table
CREATE TABLE IF NOT EXISTS RSVP (
    RSVP_id INT PRIMARY KEY AUTO_INCREMENT,
    RSVP_status ENUM('Going', 'Interested', 'Not Going') NOT NULL,
    user_id INT NOT NULL,
    event_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES User(user_id),
    FOREIGN KEY (event_id) REFERENCES Event(event_id)
);

-- Indexes for improved query performance
CREATE INDEX IF NOT EXISTS idx_rsvp_user_id ON RSVP(user_id);
CREATE INDEX IF NOT EXISTS idx_rsvp_event_id ON RSVP(event_id);
CREATE INDEX IF NOT EXISTS idx_rsvp_status ON RSVP(RSVP_status);
CREATE INDEX IF NOT EXISTS idx_rsvp_user_event ON RSVP(user_id, event_id);