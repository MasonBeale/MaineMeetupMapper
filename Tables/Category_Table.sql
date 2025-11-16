-- Author: Kristina Zbinden using Perplexity AI
-- Schema for Category Table with indexing for search by updated_at and created_at

CREATE TABLE IF NOT EXISTS Category (
    category_id INT PRIMARY KEY AUTO_INCREMENT,
    category_name VARCHAR(100) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_created_at (created_at),
    INDEX idx_updated_at (updated_at) asfdf
);