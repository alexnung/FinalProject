-- 1. Users Table
CREATE TABLE Users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('Admin', 'Manager', 'Staff') NOT NULL,
    email VARCHAR(255) NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 2. Product_Categories Table
CREATE TABLE Product_Categories (
    category_id INT AUTO_INCREMENT PRIMARY KEY,
    category_name VARCHAR(100) NOT NULL,
    description TEXT
);

-- 3. Products Table
CREATE TABLE Products (
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    product_name VARCHAR(255) NOT NULL,
    description TEXT,
    quantity_in_stock INT DEFAULT 0,
    unit_price DECIMAL(10, 2) NOT NULL,
    category_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES Product_Categories(category_id)  -- Added foreign key for product category
);

-- Altering Products table to have a new field
ALTER table products
add reorder_level int;

-- 4. Orders Table
CREATE TABLE Orders (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    customer_id INT,
    status ENUM('Pending', 'Shipped', 'Delivered','Cancelled') NOT NULL,
    total_amount DECIMAL(10, 2) NOT NULL,
    payment_status ENUM('Paid', 'Pending') NOT NULL,
    shipping_address TEXT NOT NULL
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES Users(user_id)
);

-- Creating a trigger to autocreate an invoice once and order has been made
DELIMITER $$

CREATE TRIGGER after_order_insert
AFTER INSERT ON `inventorymanagement`.`orders`
FOR EACH ROW
BEGIN
    -- Insert the invoice for the newly created order
    INSERT INTO `inventorymanagement`.`invoices` (
        `order_id`, 
        `customer_id`, 
        `invoice_date`, 
        `total_amount`, 
        `payment_status`
    ) VALUES (
        NEW.order_id,                -- Copy over order ID
        NEW.customer_id,             -- Copy over customer ID
        NEW.order_date,              -- Use the order date as the invoice date
        NEW.total_amount,            -- Copy over total amount from the order
        NEW.payment_status           -- Copy over payment status from the order
    );

    -- Update the formatted_invoice_id in the newly created invoice
    UPDATE `inventorymanagement`.`invoices`
    SET formatted_invoice_id = CONCAT('INV', LPAD(LAST_INSERT_ID(), 5, '0'))
    WHERE invoice_id = LAST_INSERT_ID();
END $$

DELIMITER ;

-- Creating a trigger updating an invoice when an order is updated
DELIMITER $$

CREATE TRIGGER update_invoice_after_order_update
AFTER UPDATE ON orders
FOR EACH ROW
BEGIN
    -- Update the corresponding invoice if the order changes
    UPDATE invoices
    SET 
        customer_id = NEW.customer_id,
        total_amount = NEW.total_amount,
        payment_status = NEW.payment_status
    WHERE order_id = NEW.order_id;
END$$

DELIMITER ;

-- 5. Order_Items Table (Many-to-many relationship between Orders and Products)
CREATE TABLE Order_Items (
    order_item_id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT,
    product_id INT,
    quantity INT NOT NULL,
    unit_price DECIMAL(10, 2) NOT NULL,
    subtotal DECIMAL(10, 2) GENERATED ALWAYS AS (quantity * unit_price) STORED,
    FOREIGN KEY (order_id) REFERENCES Orders(order_id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES Products(product_id) ON DELETE CASCADE
);

-- 7. Reports Table (Store generated reports)
CREATE TABLE Reports (
    report_id INT AUTO_INCREMENT PRIMARY KEY,
    report_type VARCHAR(100) NOT NULL,
    generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    user_id INT,
    report_data TEXT,
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

-- 9. Invoices Table
CREATE TABLE Invoices (
    invoice_id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL, -- Link to the related order
    customer_id INT NOT NULL, -- Link to the customer who placed the order
    invoice_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Date the invoice is generated
    total_amount DECIMAL(10, 2) NOT NULL, -- Total amount of the invoice
    payment_status ENUM('Paid', 'Pending') NOT NULL, -- Payment status of the invoice
    FOREIGN KEY (order_id) REFERENCES Orders(order_id) ON DELETE CASCADE,
    FOREIGN KEY (customer_id) REFERENCES Users(user_id) ON DELETE CASCADE
);
