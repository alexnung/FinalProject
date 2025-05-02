-- Invalid Inserts for Testing Database Constraints

-- Users Table: Missing `username`
INSERT INTO Users (password_hash, role, email)
VALUES ('hashed_password1', 'Admin', 'admin@example.com');

-- Users Table: Invalid value for `role`
INSERT INTO Users (username, password_hash, role, email)
VALUES ('invalid_role_user', 'hashed_password2', 'SuperAdmin', 'user@example.com');

-- Product_Categories Table: Exceeding length of `category_name`
INSERT INTO Product_Categories (category_name, description)
VALUES ('A very long category name exceeding 100 characters which is not allowed. Lorem ipsum Lorem ipsum Lorem ipsum Lorem ipsum', 'Some description');

-- Products Table: Invalid `category_id`
INSERT INTO Products (product_name, description, quantity_in_stock, unit_price, category_id)
VALUES ('Invalid Category Product', 'A product with a non-existent category', 10, 19.99, 999);

-- Orders Table: Missing `total_amount`
INSERT INTO Orders (customer_id, status, payment_status, shipping_address)
VALUES (1, 'Pending', 'Paid', '123 Main Street');

-- Stock_Transactions Table: Invalid `product_id`
INSERT INTO Stock_Transactions (product_id, transaction_type, quantity, user_id, reason)
VALUES (999, 'Sale', 5, 1, 'Invalid product');

-- End of Invalid Test Script
