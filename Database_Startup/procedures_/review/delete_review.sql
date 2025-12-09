/*
delete_review.sql 
Deleation procedures for review table
@author Mason Beale
*/
DELIMITER //
CREATE PROCEDURE IF NOT EXISTS delete_review (
    p_review_id INT
)
BEGIN
    DELETE FROM review WHERE review_id = p_review_id;
END//
DELIMITER ;