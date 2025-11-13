-- Event table creation
CREATE TABLE Event (
    event_id INT PRIMARY KEY AUTO_INCREMENT,
    event_name VARCHAR(150) NOT NULL,
    event_date DATE NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME,
    max_capacity INT,
    organizer_id INT NOT NULL,
    location_id INT NOT NULL,
    description VARCHAR(750),
    FOREIGN KEY (organizer_id) REFERENCES User(user_id),
    FOREIGN KEY (location_id) REFERENCES Location(location_id)
);

/*
Event index creation scripts
*/

-- Date to query events by date
CREATE INDEX IX_Event_Date
ON Event (event_date);

-- Organizer to query events by organizer
CREATE INDEX IX_Event_OrganizerID
ON Event (organizer_id);

-- Location to query events by location
CREATE INDEX IX_Event_LocationID
ON Event (location_id);



-- Exmaple Queries

-- Get all events between January 20, 2026 and April 20, 2026
SELECT *
FROM Event
WHERE event_date BETWEEN '2026-01-20' AND '2026-04-20';

-- Get all events with capacity between 100-200
SELECT *
FROM Event
WHERE max_capacity BETWEEN 100 AND 200;

-- Get all events in Portland, Maine
SELECT Event.*
FROM Event
JOIN Location ON Event.location_id = Location.location_id
WHERE Location.city = 'Portland' AND Location.state = 'Maine';
