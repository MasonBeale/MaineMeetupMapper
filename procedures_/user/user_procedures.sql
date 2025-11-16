-- Author: Kristina Zbinden using Perplexity AI
-- CRUD Procedures for User Table

-- Create
DELIMITER //
CREATE PROCEDURE CreateUser (
    IN p_username VARCHAR(50),
    IN p_email VARCHAR(100),
    IN p_password_hash VARCHAR(255),
    IN p_first_name VARCHAR(50),
    IN p_last_name VARCHAR(50)
)

BEGIN
    INSERT INTO User (username, email, password_hash, first_name, last_name)
    VALUES (p_username, p_email, p_password_hash, p_first_name, p_last_name);
END //
DELIMITER ;

-- Read
DELIMITER //
CREATE PROCEDURE GetUserById (
    IN p_user_id INT
)
BEGIN
    SELECT * FROM User WHERE user_id = p_user_id;
END //
DELIMITER ;

-- Update
DELIMITER //
CREATE PROCEDURE UpdateUser (
    IN p_user_id INT,
    IN p_username VARCHAR(50),
    IN p_email VARCHAR(100),
    IN p_password_hash VARCHAR(255),
    IN p_first_name VARCHAR(50),
    IN p_last_name VARCHAR(50)
)
BEGIN
    UPDATE User
    SET username = p_username,
        email = p_email,
        password_hash = p_password_hash,
        first_name = p_first_name,
        last_name = p_last_name,
        updated_at = CURRENT_TIMESTAMP
    WHERE user_id = p_user_id;
END //
DELIMITER ;

-- Delete
DELIMITER //
CREATE PROCEDURE DeleteUser (
    IN p_user_id INT
)
BEGIN
    DELETE FROM User WHERE user_id = p_user_id;
END //
DELIMITER ;