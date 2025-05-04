# FinalProject

# Individual Coursework

## Overview
The Inventory Management System (IMS) is a Python-based project that provides a backend API for managing users, products, categories, orders, invoices, and transactions in a retail business. The system uses MySQL as the database and Flask as the web framework, offering a RESTful API for CRUD operations.

---

## Table of Contents

1. [Introduction](#introduction)
2. [Features](#features)
3. [Installation](#installation)
4. [Usage](#usage)
5. [API Endpoints](#api-endpoints)
6. [Usage Examples](#usage-examples)
7. [Contribution Guidelines](#contribution-guidelines)
8. [Credits](#credits)
9. [License](#license)
10. [Contact](#contact)

---

## Introduction

The Inventory Management System simplifies inventory tracking, user management, order processing, and more. It includes an interactive REST API for seamless integration with other systems or frontend applications. The system is designed to be extensible and scalable, with built-in support for error handling and modular code structure.

---

## Features

- **CRUD Operations**:
  - Manage Users, Products, Categories, Orders, Order Items, Stock Transactions, Reports, Transactions, and Invoices.
  
- **Database Integration**:
  - MySQL database for reliable and efficient data storage.

- **REST API**:
  - A Flask-based API for easy interaction with the backend.

- **Reusability**:
  - Centralized utility functions for database connectivity and query execution.

- **Error Handling**:
  - Comprehensive error-handling for robust operation.

- **Modular Design**:
  - Code is structured for maintainability and scalability.

---

## Installation

### Prerequisites

- Python 3.8 or later
- MySQL Server 8.0 or later
- Node.js (if integrating with a frontend)

### Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/alexnung/FinalProject.git

2. Install software:
   Install Python - https://www.python.org/downloads/
   Install MySQL server or Workbench- https://www.oracle.com/mysql/technologies/mysql-enterprise-edition-downloads.html#windows

3. Install dependencies:
   ```bash
   Run "pip install flask"
   Run "pip install flask mysql-connector-python"
   Run "pip install flask-cors"

4. Setup database:
   Run  TableCreation.sql code in MySQL Workbench

5. Setup database:
   Configure settings in db_util.py so host, user, password and database name match local settings (can be found in MySQL Workbench)

### Usage
   Run  "python app.py" in the folder "app" in the project

## API-Endpoints
. Users
    GET /users - Fetch all users.
    GET /users/<user_id> - Fetch a specific user.
    POST /users - Create a new user.
    PUT /users/<user_id> - Update a user.
    DELETE /users/<user_id> - Delete a user.

. Products
    GET /products - Fetch all products.
    GET /products/<product_id> - Fetch a specific product.
    POST /products - Add a new product.
    PUT /products/<product_id> - Update a product.
    DELETE /products/<product_id> - Delete a product.

Endpoints for categories, orders, stock transactions, reports, transactions, and invoices follow a similar structure.

## Usage-Examples
    . Fetch All Products
    curl http://127.0.0.1:5000/products

    . Add a New User
    curl -X POST http://127.0.0.1:5000/users -H "Content-Type: application/json" -d '{
    "username": "johndoe",
    "password": "password123",
    "email": "johndoe@example.com",
    "role": "Manager",
    "first_name": "John",
    "last_name": "Doe"
    }'

    . Update on Order Status
    curl -X PUT http://127.0.0.1:5000/orders/1 -H "Content-Type: application/json" -d '{
    "status": "Shipped"
    }'

## Contribution-Guidelines
I welcome contributions! Follow these steps to contribute:

1. Fork the repository - Link (https://github.com/alexnung/FinalProject).

2. Create a new branch:
    run "git checkout -b feature/your-feature-name"

3. Commit changes:
    run "git commit -m "Add your feature description""

4. Push to branch:
    run "git push origin feature/your-feature-name"

5. Open a pull request:
    Ensure the code follows existing style and has the necessary tests.

## Credits
Thank you to:
Dimitrios Airantzis for Guidance on the project.
Keith Mannock and Tingting Han from the department of Computer Science at Birkbeck for the lectures, providing a basis knowledge for the coursework.

## License
This project is developed as part of an academic assignment and is intended for educational purposes only. The code and materials provided are restricted to evaluation and learning activities within the university. Redistribution, modification, or use for commercial purposes is not permitted without prior consent.

## Contact
For any queries, feel free to reach out:

Email: anung01@student.bbk.ac.uk
GitHub: alexnung

This README provides comprehensive information, making it user-friendly for developers and contributors alike. Let me know if you need further details!