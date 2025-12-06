/*
analytics.sql 
Alters tables to include analytics attributes
Creates procedures to update those attributes
@author Mason Beale
*/
ALTER TABLE users ADD COLUMN last_login DATETIME;
ALTER TABLE events ADD COLUMN view_count INT DEFAULT 0;

DELIMITER //
CREATE PROCEDURE IF NOT EXISTS user_login (p_user_id INT)
BEGIN
  UPDATE users SET last_login = NOW() WHERE user_id = p_user_id;
END//
DELIMITER ;

DELIMITER //
CREATE PROCEDURE IF NOT EXISTS increment_event_view_count (p_event_id INT)
BEGIN
  UPDATE events SET view_count = view_count + 1 WHERE event_id = p_event_id;
END//
DELIMITER ;