/*
review_table.sql 
Creates the review table and indexes for the table
@author Mason Beale
*/
CREATE TABLE IF NOT EXISTS review (
    review_id INT PRIMARY KEY AUTO_INCREMENT,
    rating INT CHECK (rating >= 1 AND rating <= 5) NOT NULL,
    comments VARCHAR(300),
    user_id INT NOT NULL,
    event_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES User(user_id),
    FOREIGN KEY (event_id) REFERENCES Event(event_id)
);

CREATE INDEX IF NOT EXISTS idx_review_user_id ON review(user_id);
CREATE INDEX IF NOT EXISTS idx_review_event_id ON review(event_id);
CREATE INDEX IF NOT EXISTS idx_review_rating ON review(rating);
CREATE INDEX IF NOT EXISTS idx_review_user_event ON review(user_id, event_id);