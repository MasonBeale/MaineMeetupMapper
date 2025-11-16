-- adding a new review to the review table
DELIMITER //
CREATE PROCEDURE IF NOT EXISTS create_review (
  p_rating INT,
  p_comments VARCHAR(300),
  p_user_id INT,
  p_event_id INT
)
BEGIN
  INSERT INTO
    review (rating, comments, user_id, event_id)
  VALUES
    (p_rating, p_comments, p_user_id, p_event_id);
END//
DELIMITER ;