-- ============================================================
-- Location Stored Procedures
-- ============================================================
-- Author: Logan
-- Date: November 13, 2025
-- Purpose: Stored procedures for Location table operations
-- ============================================================

USE meetup_mapper;

DELIMITER //

-- Procedure to add a new location
CREATE PROCEDURE AddNewLocation(
    IN p_venue_name VARCHAR(255),
    IN p_address VARCHAR(255),
    IN p_city VARCHAR(100),
    IN p_zip_code VARCHAR(10)
)
BEGIN
    INSERT INTO Location (venue_name, address, city, zip_code)
    VALUES (p_venue_name, p_address, p_city, p_zip_code);
    
    SELECT LAST_INSERT_ID() as new_location_id;
END//

DELIMITER ;

-- Example usage:
-- CALL AddNewLocation('Port City Music Hall', '504 Congress St', 'Portland', '04101');