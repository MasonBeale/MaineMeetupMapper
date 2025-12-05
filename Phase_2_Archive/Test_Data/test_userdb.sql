-- Author: Kristina Zbinden using Perplexity AI
-- Test script for User table CRUD procedures
-- Run after loading schema and procedures

-- Cleanup test data if exists (optional)
DELETE FROM User WHERE username LIKE 'testuser%' OR username LIKE 'updateduser%';

-- CREATE Tests
CALL CreateUser('testuser1', 'test1@example.com', 'hashedpass1', 'Test', 'User');
CALL CreateUser('testuser2', 'test2@example.com', 'hashedpass2', 'Sample', 'Account');

-- READ Tests
CALL GetUserById(1);
CALL GetUserById(2);

-- UPDATE Test
CALL UpdateUser(1, 'updateduser1', 'updated1@example.com', 'updatedhash1', 'Updated', 'Name');

-- Verify update
CALL GetUserById(1);

-- DELETE Test
CALL DeleteUser(2);

-- Verify delete
CALL GetUserById(2); -- Should return empty

-- Check remaining data
SELECT * FROM User;

-- Cleanup test data after tests
-- DELETE FROM User WHERE username LIKE 'testuser%' OR username LIKE 'updateduser%';