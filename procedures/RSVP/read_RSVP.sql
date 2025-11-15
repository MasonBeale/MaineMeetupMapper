-- gets a RSVP by its ID
DELIMITER //
CREATE PROCEDURE IF NOT EXISTS read_RSVP_by_id (
    p_RSVP_id INT
)
BEGIN
    SELECT * FROM RSVP WHERE RSVP_id = p_RSVP_id;
END//
DELIMITER ;

-- gets all RSVP for a specific event
DELIMITER //
CREATE PROCEDURE IF NOT EXISTS read_RSVP_by_event_id (
    p_event_id INT
)
BEGIN
    SELECT * FROM review WHERE event_id = p_event_id;
END//
DELIMITER ;

-- gets all RSVP made by a specific user
DELIMITER //
CREATE PROCEDURE IF NOT EXISTS read_RSVP_by_user_id (
    p_user_id INT
)
BEGIN
    SELECT * FROM RSVP WHERE user_id = p_user_id;
END//
DELIMITER ;