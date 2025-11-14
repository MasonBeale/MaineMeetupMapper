-- delete a review by its ID
DELIMITER //
CREATE PROCEDURE delete_review (
    p_review_id INT
)
BEGIN
    DELETE FROM review WHERE review_id = p_review_id;
END//
DELIMITER ;