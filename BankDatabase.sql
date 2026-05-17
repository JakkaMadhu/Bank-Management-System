-- Database schema for Bank Management System
CREATE DATABASE IF NOT EXISTS dbbankmanagement;
USE dbbankmanagement;

-- Admin credentials table
CREATE TABLE IF NOT EXISTS admin_info (
    name VARCHAR(32) NOT NULL,
    pin INT NOT NULL,
    PRIMARY KEY (name)
);

-- User account information table
CREATE TABLE IF NOT EXISTS user_bank_info (
    name VARCHAR(32) NOT NULL,
    account_number INT NOT NULL PRIMARY KEY,
    account_type VARCHAR(32) NOT NULL,
    account_balance INT NOT NULL DEFAULT 0,
    account_pin INT NOT NULL,
    date_of_create DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Transaction history table
CREATE TABLE IF NOT EXISTS transaction_details (
    transaction_number INT NOT NULL PRIMARY KEY,
    account_number INT NOT NULL,
    transaction_type VARCHAR(32) NOT NULL,
    amount INT NOT NULL,
    date_of_transaction DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (account_number) REFERENCES user_bank_info(account_number)
);

-- Example data (uncomment and modify values if needed)
-- INSERT INTO admin_info (name, pin)
-- VALUES ('admin', 1234)
-- ON DUPLICATE KEY UPDATE pin = VALUES(pin);

-- INSERT INTO user_bank_info (name, account_number, account_type, account_balance, account_pin)
-- VALUES ('Customer Name', 2345, 'savings', 2000, 1234);

-- INSERT INTO transaction_details (transaction_number, account_number, transaction_type, amount)
-- VALUES (1, 2345, 'deposit', 10000);

-- Schema inspection queries
-- SELECT * FROM admin_info;
-- SELECT * FROM user_bank_info;
-- SELECT * FROM transaction_details;
-- DESCRIBE transaction_details;
-- DESCRIBE user_bank_info;
