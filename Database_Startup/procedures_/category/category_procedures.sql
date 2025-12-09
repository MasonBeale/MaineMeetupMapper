-- Author: Kristina Zbinden using Perplexity AI
-- CRUD Procedures for Category Table

-- Create
DELIMITER //
CREATE PROCEDURE CreateCategory (
    IN p_category_name VARCHAR(100)
)
BEGIN
    INSERT INTO Category (category_name)
    VALUES (p_category_name);
END //
DELIMITER ;

-- Read
DELIMITER //    
CREATE PROCEDURE GetCategoryById (
    IN p_category_id INT
)
BEGIN
    SELECT * FROM Category WHERE category_id = p_category_id;
END //
DELIMITER ;

-- Update
DELIMITER //
CREATE PROCEDURE UpdateCategory (
    IN p_category_id INT,
    IN p_category_name VARCHAR(100)
)   
BEGIN
    UPDATE Category
    SET category_name = p_category_name,
        updated_at = CURRENT_TIMESTAMP
    WHERE category_id = p_category_id;
END //  
DELIMITER ;

-- Delete 
DELIMITER //
CREATE PROCEDURE DeleteCategory (
    IN p_category_id INT
)
BEGIN
    DELETE FROM Category WHERE category_id = p_category_id;
END //
DELIMITER ;

