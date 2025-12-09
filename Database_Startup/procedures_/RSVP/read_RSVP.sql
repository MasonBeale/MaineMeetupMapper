/*
read_RSVP.sql 
Read procedures for RSVP table
@author Mason Beale
*/
DELIMITER //
CREATE PROCEDURE IF NOT EXISTS read_RSVP_by_id (
    p_RSVP_id INT
)
BEGIN
    SELECT * FROM RSVP WHERE RSVP_id = p_RSVP_id;
END//
DELIMITER ;

DELIMITER //
CREATE PROCEDURE IF NOT EXISTS read_RSVP_by_event_id (
    p_event_id INT
)
BEGIN
    SELECT * FROM RSVP USE INDEX (idx_rsvp_event_id) WHERE event_id = p_event_id;
END//
DELIMITER ;

DELIMITER //
CREATE PROCEDURE IF NOT EXISTS read_RSVP_by_user_id (
    p_user_id INT
)
BEGIN
    SELECT * FROM RSVP USE INDEX (idx_rsvp_user_id) WHERE user_id = p_user_id;
END//
DELIMITER ;