-- just making the RSVP table
CREATE TABLE IF NOT EXISTS RSVP (
    RSVP_id INT PRIMARY KEY AUTO_INCREMENT,
    RSVP_status ENUM('Going', 'Interested', 'Not Going') NOT NULL,
    user_id INT NOT NULL,
    event_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES User(user_id),
    FOREIGN KEY (event_id) REFERENCES Event(event_id)
);