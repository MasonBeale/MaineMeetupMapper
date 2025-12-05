-- Author: Kristina Zbinden using Perplexity AI
-- Test script for Category table CRUD procedures
-- Run after loading schema and procedures

-- Cleanup test data if exists
DELETE FROM Category WHERE category_name LIKE 'TestCategory%';

-- CREATE Tests
CALL CreateCategory('TestCategory1');
CALL CreateCategory('TestCategory2');

-- READ Tests
CALL GetCategoryById(1);
CALL GetCategoryById(2);

-- UPDATE Test
CALL UpdateCategory(1, 'UpdatedCategory1');

-- Verify update
CALL GetCategoryById(1);

-- DELETE Test
CALL DeleteCategory(2);

-- Verify delete
CALL GetCategoryById(2); -- Should return empty

-- Check remaining data
SELECT * FROM Category;

-- Cleanup test data
-- DELETE FROM Category WHERE category_name LIKE 'TestCategory%';