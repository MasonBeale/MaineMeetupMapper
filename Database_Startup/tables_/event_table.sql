-- Author Philip Lane and Claude Sonnet 4.5
-- A small SQL schema for creating the Event table for Maine Meetup Mapper.

CREATE TABLE IF NOT EXISTS Event (
    event_id INT PRIMARY KEY AUTO_INCREMENT,
    event_name VARCHAR(150) NOT NULL,
    event_date DATE NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME,
    max_capacity INT CHECK (max_capacity > 0),
    organizer_id INT,
    location_id INT NOT NULL,
    description VARCHAR(750),
    CONSTRAINT chk_event_times CHECK (end_time > start_time),
    FOREIGN KEY (organizer_id) REFERENCES User(user_id),
    FOREIGN KEY (location_id) REFERENCES Location(location_id)
);
