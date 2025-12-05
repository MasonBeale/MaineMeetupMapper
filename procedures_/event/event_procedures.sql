-- Author Philip Lane and Claude Sonnet 4.5

-- CREATE

DELIMITER //
CREATE PROCEDURE InsertEvent(
    IN p_event_name VARCHAR(150),
    IN p_event_date DATE,
    IN p_start_time TIME,
    IN p_end_time TIME,
    IN p_max_capacity INT,
    IN p_organizer_id INT,
    IN p_location_id INT,
    IN p_description VARCHAR(750)
)
BEGIN
    INSERT INTO Event (event_name, event_date, start_time, end_time, max_capacity, 
                       organizer_id, location_id, description)
    VALUES (p_event_name, p_event_date, p_start_time, p_end_time, p_max_capacity,
            p_organizer_id, p_location_id, p_description);
END //
DELIMITER ;

-- Read

DELIMITER //
CREATE PROCEDURE GetEventById(IN p_event_id INT)
BEGIN
    SELECT * FROM Event WHERE event_id = p_event_id;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE GetEventsByDateRange(
    IN p_start_date DATE,
    IN p_end_date DATE
)
BEGIN
    SELECT * FROM Event 
    WHERE event_date BETWEEN p_start_date AND p_end_date
    ORDER BY event_date, start_time;
END //

-- Update

DELIMITER //
CREATE PROCEDURE UpdateEvent(
    IN p_event_id INT,
    IN p_event_name VARCHAR(150),
    IN p_event_date DATE,
    IN p_start_time TIME,
    IN p_end_time TIME,
    IN p_max_capacity INT,
    IN p_location_id INT,
    IN p_description VARCHAR(750)
)
BEGIN
    UPDATE Event
    SET event_name = p_event_name,
        event_date = p_event_date,
        start_time = p_start_time,
        end_time = p_end_time,
        max_capacity = p_max_capacity,
        location_id = p_location_id,
        description = p_description
    WHERE event_id = p_event_id;
END //
DELIMITER ;

-- DELETE

DELIMITER //
CREATE PROCEDURE DeleteEvent(IN p_event_id INT)
BEGIN
    DELETE FROM Event WHERE event_id = p_event_id;
END //
DELIMITER ;
