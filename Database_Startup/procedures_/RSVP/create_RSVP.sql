/*
create_RSVP.sql 
Creation procedures for RSVP table
@author Mason Beale
*/
DELIMITER //
CREATE PROCEDURE IF NOT EXISTS create_RSVP (
  p_rsvp_status ENUM('Going', 'Interested', 'Not Going'),
  p_user_id INT,
  p_event_id INT
)
BEGIN
  INSERT INTO
    RSVP (rsvp_status, user_id, event_id)
  VALUES
    (p_rsvp_status, p_user_id, p_event_id);
END//
DELIMITER ;