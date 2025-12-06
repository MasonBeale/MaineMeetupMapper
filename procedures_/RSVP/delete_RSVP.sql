/*
delete_RSVP.sql 
Deleation procedures for RSVP table
@author Mason Beale
*/
DELIMITER //
CREATE PROCEDURE IF NOT EXISTS delete_RSVP (
    p_RSVP_id INT
)
BEGIN
    DELETE FROM RSVP WHERE RSVP_id = p_RSVP_id;
END//
DELIMITER ;