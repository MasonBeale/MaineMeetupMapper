-- updates the rating and comments of an existing review by ID
CREATE PROCEDURE IF NOT EXISTS update_review (
    p_review_id INT,
    p_rating INT,
    p_comments VARCHAR(300)
)
BEGIN
    UPDATE review SET rating = p_rating, comments = p_comments WHERE review_id = p_review_id;
END;