/*
read_review.sql 
Read procedures for review table
@author Mason Beale
*/
DELIMITER //
CREATE PROCEDURE IF NOT EXISTS read_review_by_id (
    p_review_id INT
)
BEGIN
    SELECT * FROM review WHERE review_id = p_review_id;
END//
DELIMITER ;

-- gets all reviews for a specific event
DELIMITER //
CREATE PROCEDURE IF NOT EXISTS read_reviews_by_event_id (
    p_event_id INT
)
BEGIN
    SELECT * FROM review USE INDEX (idx_review_event_id) WHERE event_id = p_event_id;
END//
DELIMITER ;

-- gets all reviews made by a specific user
DELIMITER //
CREATE PROCEDURE IF NOT EXISTS read_reviews_by_user_id (
    p_user_id INT
)
BEGIN
    SELECT * FROM review USE INDEX (idx_review_user_id) WHERE user_id = p_user_id;
END//
DELIMITER ;