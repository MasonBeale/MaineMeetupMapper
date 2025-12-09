/*
analytics.sql 
Alters tables to include analytics attributes
Creates procedures to update those attributes
@author Mason Beale
*/
ALTER TABLE User ADD COLUMN last_login DATETIME;
ALTER TABLE Event ADD COLUMN view_count INT DEFAULT 0;

DELIMITER //
CREATE PROCEDURE IF NOT EXISTS user_login (p_user_id INT)
BEGIN
  UPDATE User SET last_login = NOW() WHERE user_id = p_user_id;
END//
DELIMITER ;

DELIMITER //
CREATE PROCEDURE IF NOT EXISTS increment_event_view_count (p_event_id INT)
BEGIN
  UPDATE Event SET view_count = view_count + 1 WHERE event_id = p_event_id;
END//
DELIMITER ;