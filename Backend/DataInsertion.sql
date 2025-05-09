-- Insert test data into Users Table
INSERT INTO Users (username, password, role, email, first_name, last_name)
VALUES 
    ('admin', 'hashed_password1', 'Admin', 'admin@example.com', 'Alice', 'Admin'),
    ('manager', 'hashed_password2', 'Manager', 'manager@example.com', 'Bob', 'Manager'),
    ('staff1', 'hashed_password3', 'Staff', 'staff1@example.com', 'Charlie', 'Staff')

-- Insert test data into Product_Categories Table
INSERT INTO Product_Categories (category_name, description)
VALUES 
    ('Electronics', 'Devices and gadgets'),
    ('Furniture', 'Home and office furniture'),
    ('Stationery', 'Office supplies and stationery items');

-- Insert test data into Products Table
INSERT INTO Products (product_name, description, quantity_in_stock, unit_price, category_id)
VALUES 
    ('Laptop', 'High performance laptop', 10, 999.99, 1),
    ('Smartphone', 'Latest model smartphone', 20, 699.99, 1),
    ('Office Chair', 'Ergonomic office chair', 15, 149.99, 2),
    ('Desk', 'Spacious office desk', 5, 299.99, 2),
    ('Notebook', '100-page notebook', 50, 2.99, 3),
    ('Pen', 'Blue ink ballpoint pen', 100, 0.99, 3);

-- Insert test data into Orders Table
INSERT INTO Orders (customer_id, status, total_amount, payment_status, shipping_address)
VALUES 
    (4, 'Pending', 1029.98, 'Pending', '123 Main Street, Cityville'),
    (4, 'Shipped', 150.97, 'Paid', '123 Main Street, Cityville');

-- Insert test data into Order_Items Table
INSERT INTO Order_Items (order_id, product_id, quantity, unit_price)
VALUES 
    (1, 1, 1, 999.99),  -- 1 Laptop
    (1, 6, 30, 0.99),   -- 30 Pens
    (2, 3, 1, 149.99);  -- 1 Office Chair

-- Insert test data into Stock_Transactions Table
INSERT INTO Stock_Transactions (product_id, transaction_type, quantity, user_id, reason)
VALUES 
    (1, 'Sale', -1, 4, 'Customer Order'),
    (6, 'Sale', -30, 4, 'Customer Order'),
    (3, 'Sale', -1, 4, 'Customer Order'),
    (1, 'Restock', 10, 2, 'Inventory Restock'),
    (6, 'Restock', 50, 2, 'Inventory Restock');

-- Insert test data into Reports Table
INSERT INTO Reports (report_type, user_id, report_data)
VALUES 
    ('Sales Summary', 1, '{"total_sales": 3, "total_revenue": 1029.98}'),
    ('Stock Overview', 1, '{"low_stock_items": 2, "out_of_stock_items": 0}');

-- Insert test data into Transactions Table
INSERT INTO Transactions (order_id, payment_date, amount, payment_method, payment_status)
VALUES 
    (1, NOW(), 1029.98, 'Credit Card', 'Paid'),
    (2, NOW(), 150.97, 'PayPal', 'Paid');

-- Insert test data into Invoices Table
INSERT INTO Invoices (order_id, customer_id, total_amount, payment_status)
VALUES 
    (1, 4, 1029.98, 'Paid'),
    (2, 4, 150.97, 'Paid');

-- Inserting value into the new reorder_level field in products
UPDATE Products
SET reorder_level = 
    CASE 
        WHEN product_id = 1 THEN 5  -- Laptop
        WHEN product_id = 2 THEN 10 -- Smartphone
        WHEN product_id = 3 THEN 3  -- Office Chair
        WHEN product_id = 4 THEN 2  -- Desk
        WHEN product_id = 5 THEN 20 -- Notebook
        WHEN product_id = 6 THEN 50 -- Pen
        ELSE 0
    END;
