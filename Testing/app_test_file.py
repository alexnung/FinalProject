import unittest
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock
import os
import re

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.app import app, create_connection  # Ensure app is correctly imported

class TestAPI(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()  # Initialize the test client
        self.client.testing = True
        self.mock_connection = MagicMock()
        self.mock_cursor = MagicMock()             

    @patch("app.app.create_connection")  # Updated patch path to app.app.create_connection
    def test_create_user(self, mock_create_connection):
        # Mock database connection and cursor
        mock_create_connection.return_value = self.mock_connection
        self.mock_connection.cursor.return_value = self.mock_cursor
        self.mock_cursor.lastrowid = 1  # Simulate a fixed user_id for the created user

        # Mock data input
        mock_data = {
            "username": "newuser",
            "password": "securepassword",
            "role": "admin",
            "email": "newuser@example.com",
            "first_name": "New",
            "last_name": "User"
        }

        # Call the endpoint
        response = self.client.post("/api/users", json=mock_data)

        # Assertions
        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.json,
            {"message": "User created successfully.", "user_id": 1}
        )
        self.mock_cursor.execute.assert_called_with(
            """
            INSERT INTO Users (username, password, role, email, first_name, last_name)
            VALUES (%s, %s, %s, %s, %s, %s);
            """,
            ("newuser", "securepassword", "admin", "newuser@example.com", "New", "User")
        )

    @patch("app.app.create_connection")  # Updated patch path to app.app.create_connection
    def test_get_all_users(self, mock_create_connection):
        # Mock database connection and cursor
        mock_create_connection.return_value = self.mock_connection
        self.mock_connection.cursor.return_value = self.mock_cursor
        self.mock_cursor.fetchall.return_value = [
            {"user_id": 1, "username": "testuser", "email": "testuser@example.com"}
        ]
        
        # Call the endpoint
        response = self.client.get("/api/users")
        
        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json,
            [{"user_id": 1, "username": "testuser", "email": "testuser@example.com"}]
        )
        self.mock_cursor.execute.assert_called_with("SELECT * FROM Users;")
        
    @patch("app.app.create_connection")
    def test_get_single_user(self, mock_create_connection):
        # Mock database connection and cursor
        mock_create_connection.return_value = self.mock_connection
        self.mock_connection.cursor.return_value = self.mock_cursor
        self.mock_cursor.fetchone.return_value = {
            "user_id": 1, 
            "username": "testuser", 
            "password": "hashedpassword", 
            "role": "admin", 
            "email": "testuser@example.com", 
            "first_name": "Test", 
            "last_name": "User"
        }

        # Call the endpoint
        response = self.client.get("/api/users/testuser")

        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json,
            {
                "user_id": 1,
                "username": "testuser",
                "password": "hashedpassword",
                "role": "admin",
                "email": "testuser@example.com",
                "first_name": "Test",
                "last_name": "User"
            }
        )
        self.mock_cursor.execute.assert_called_with(
            "SELECT * FROM Users WHERE username = %s;", ("testuser",)
        )

    @patch("app.app.create_connection")  # Updated patch path to app.app.create_connection
    def test_update_user(self, mock_create_connection):
        # Mock database connection and cursor
        mock_create_connection.return_value = self.mock_connection
        self.mock_connection.cursor.return_value = self.mock_cursor
        self.mock_cursor.rowcount = 1  # Simulate a successful update
        
        # Mock data input
        mock_data = {
            "username": "updateduser",
            "password": "newpassword",
            "role": "admin",
            "email": "updateduser@example.com",
            "first_name": "Updated",
            "last_name": "User"
        }
        
        # Call the endpoint
        response = self.client.put("/api/users/updateduser", json=mock_data)
        
        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json,
            {"message": "User updated successfully."}
        )
        self.mock_cursor.execute.assert_called_with(
            """
            UPDATE Users
            SET username = %s, password = %s, role = %s, email = %s, first_name = %s, last_name = %s
            WHERE username = %s;
            """,
            ("updateduser", "newpassword", "admin", "updateduser@example.com", "Updated", "User", "updateduser")
        )

    @patch("app.app.create_connection")  # Updated patch path to app.app.create_connection
    def test_delete_user(self, mock_create_connection):
        # Mock database connection and cursor
        mock_create_connection.return_value = self.mock_connection
        self.mock_connection.cursor.return_value = self.mock_cursor
        self.mock_cursor.rowcount = 1  # Simulate a successful delete
        
        # Call the endpoint
        response = self.client.delete("/api/users/updateduser")
        
        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json,
            {"message": "User deleted successfully."}
        )
        self.mock_cursor.execute.assert_called_with(
            "DELETE FROM Users WHERE username = %s;", ("updateduser",)
        )
        
    @patch("app.app.create_connection")  # Updated patch path to app.app.create_connection
    def test_create_user_invalid_input(self, mock_create_connection):
        # Mock database connection and cursor
        mock_create_connection.return_value = self.mock_connection
        self.mock_connection.cursor.return_value = self.mock_cursor

        # Test missing required fields (POST)
        mock_data = {
            'password': 'password123',
            'role': 'user',
            'email': 'test@example.com'
        }
        response = self.client.post('/api/users', json=mock_data)
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Missing required fields', response.data)

    @patch("app.app.create_connection")  # Updated patch path to app.app.create_connection
    def test_get_user_invalid(self, mock_create_connection):
        # Mock database connection and cursor
        mock_create_connection.return_value = self.mock_connection
        self.mock_connection.cursor.return_value = self.mock_cursor
        
        # Simulate user not found
        self.mock_cursor.fetchone.return_value = None

        # Test for nonexistent user (GET)
        response = self.client.get('/api/users/nonexistent_user')  # Use /<username> here
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'User not found', response.data)

    @patch("app.app.create_connection")  # Updated patch path to app.app.create_connection
    def test_update_user_invalid_input(self, mock_create_connection):
        # Mock database connection and cursor
        mock_create_connection.return_value = self.mock_connection
        self.mock_connection.cursor.return_value = self.mock_cursor
        
        # Test for updating a nonexistent user (PUT)
        mock_data = {
            'username': 'nonexistent_user',
            'password': 'newpassword123',
            'role': 'admin',
            'email': 'newemail@example.com',
            'first_name': 'John',
            'last_name': 'Doe'
        }
        
        # Simulate no rows affected (nonexistent user)
        self.mock_cursor.rowcount = 0
        
        response = self.client.put('/api/users/nonexistent_user', json=mock_data)  # Use /<username> here
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'User not found', response.data)

        # Test for invalid input (empty username) when updating a user (PUT)
        mock_data = {
            'username': '',
            'password': 'updatedpassword123',
            'role': 'admin',
            'email': 'updateduser@example.com',
            'first_name': 'John',
            'last_name': 'Smith'
        }
        response = self.client.put('/api/users/', json=mock_data)  # Handle invalid input
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.', response.data)

    @patch("app.app.create_connection")  # Updated patch path to app.app.create_connection
    def test_delete_user_invalid(self, mock_create_connection):
        # Mock database connection and cursor
        mock_create_connection.return_value = self.mock_connection
        self.mock_connection.cursor.return_value = self.mock_cursor
        
        # Test for deleting a nonexistent user (DELETE)
        
        # Simulate no rows affected (nonexistent user)
        self.mock_cursor.rowcount = 0
        
        response = self.client.delete('/api/users/nonexistent_user')  # Use /<username> here
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'User not found', response.data)

        # Test for invalid input (empty username) when deleting a user (DELETE)
        response = self.client.delete('/api/users/', json={})  # Handle invalid input
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.', response.data)
        
    @patch("app.app.create_connection")
    def test_create_category(self, mock_create_connection):
        # Mock database connection and cursor
        mock_create_connection.return_value = self.mock_connection
        self.mock_connection.cursor.return_value = self.mock_cursor
        self.mock_cursor.lastrowid = 3

        # Mock data input
        mock_data = {"category_name": "Science", "description": "Science-related books"}

        # Call the endpoint
        response = self.client.post("/api/product_categories", json=mock_data)

        # Assertions
        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.json,
            {"message": "Category created successfully.", "category_id": 3}
        )
        self.mock_cursor.execute.assert_called_with(
            """
            INSERT INTO Product_Categories (category_name, description)
            VALUES (%s, %s);
            """,
            ("Science", "Science-related books")
        )

    @patch("app.app.create_connection")
    def test_get_all_categories(self, mock_create_connection):
        # Mock database connection and cursor
        mock_create_connection.return_value = self.mock_connection
        self.mock_connection.cursor.return_value = self.mock_cursor
        self.mock_cursor.fetchall.return_value = [
            {"category_id": 1, "category_name": "Fiction", "description": "Fictional books"},
            {"category_id": 2, "category_name": "Non-Fiction", "description": "Non-Fictional books"}
        ]

        # Call the endpoint
        response = self.client.get("/api/product_categories")

        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json,
            [
                {"category_id": 1, "category_name": "Fiction", "description": "Fictional books"},
                {"category_id": 2, "category_name": "Non-Fiction", "description": "Non-Fictional books"}
            ]
        )
        self.mock_cursor.execute.assert_called_with("SELECT * FROM Product_Categories;")

    @patch("app.app.create_connection")
    def test_get_single_category(self, mock_create_connection):
        # Mock database connection and cursor
        mock_create_connection.return_value = self.mock_connection
        self.mock_connection.cursor.return_value = self.mock_cursor
        self.mock_cursor.fetchone.return_value = {"category_id": 1, "category_name": "Fiction", "description": "Fictional books"}

        # Call the endpoint
        response = self.client.get("/api/product_categories/1")

        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json,
            {"category_id": 1, "category_name": "Fiction", "description": "Fictional books"}
        )
        self.mock_cursor.execute.assert_called_with(
            "SELECT * FROM Product_Categories WHERE category_id = %s;", (1,)
        )

    @patch("app.app.create_connection")
    def test_update_category(self, mock_create_connection):
        # Mock database connection and cursor
        mock_create_connection.return_value = self.mock_connection
        self.mock_connection.cursor.return_value = self.mock_cursor
        self.mock_cursor.rowcount = 1

        # Mock data input
        mock_data = {"category_name": "Science & Tech", "description": "Updated description"}

        # Call the endpoint
        response = self.client.put("/api/product_categories/3", json=mock_data)

        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"message": "Category updated successfully."})
        self.mock_cursor.execute.assert_called_with(
            """
            UPDATE Product_Categories
            SET category_name = %s, description = %s
            WHERE category_id = %s;
            """,
            ("Science & Tech", "Updated description", 3)
        )

    @patch("app.app.create_connection")
    def test_delete_category(self, mock_create_connection):
        # Mock database connection and cursor
        mock_create_connection.return_value = self.mock_connection
        self.mock_connection.cursor.return_value = self.mock_cursor
        self.mock_cursor.rowcount = 1

        # Call the endpoint
        response = self.client.delete("/api/product_categories/3")

        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"message": "Category deleted successfully."})
        self.mock_cursor.execute.assert_called_with(
            "DELETE FROM Product_Categories WHERE category_id = %s;", (3,)
        )
        
    @patch("app.app.create_connection")  # Updated patch path to app.app.create_connection
    def test_create_category_invalid_input(self, mock_create_connection):
        # Mock database connection and cursor
        mock_create_connection.return_value = self.mock_connection
        self.mock_connection.cursor.return_value = self.mock_cursor

        # Test missing required fields (POST)
        mock_data = {
            'description': 'Books category'  # Missing category_name
        }
        response = self.client.post('/api/product_categories', json=mock_data)
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Missing required fields', response.data)

    @patch("app.app.create_connection")  # Updated patch path to app.app.create_connection
    def test_get_category_invalid(self, mock_create_connection):
        # Mock database connection and cursor
        mock_create_connection.return_value = self.mock_connection
        self.mock_connection.cursor.return_value = self.mock_cursor
    
        # Simulate category not found
        self.mock_cursor.fetchone.return_value = None

        # Test for nonexistent category (GET)
        response = self.client.get('/api/product_categories/9999')  # Use an invalid category_id
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'Category not found', response.data)

    @patch("app.app.create_connection")  # Updated patch path to app.app.create_connection
    def test_update_category_invalid_input(self, mock_create_connection):
        # Mock database connection and cursor
        mock_create_connection.return_value = self.mock_connection
        self.mock_connection.cursor.return_value = self.mock_cursor
    
        # Test for updating a nonexistent category (PUT)
        mock_data = {
            'category_name': 'Updated Books',
            'description': 'Updated description'
        }
    
        # Simulate no rows affected (nonexistent category)
        self.mock_cursor.rowcount = 0
    
        response = self.client.put('/api/product_categories/9999', json=mock_data)  # Use an invalid category_id
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'Category not found', response.data)

        # Test for invalid input (empty category_id) when updating a category (PUT)
        mock_data = {
            'category_name': 'Updated Books',
            'description': 'Updated description'
        }
        response = self.client.put('/api/product_categories/', json=mock_data)  # Missing category_id
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.', response.data)

    @patch("app.app.create_connection")  # Updated patch path to app.app.create_connection
    def test_delete_category_invalid(self, mock_create_connection):
        # Mock database connection and cursor
        mock_create_connection.return_value = self.mock_connection
        self.mock_connection.cursor.return_value = self.mock_cursor
    
        # Test for deleting a nonexistent category (DELETE)
        self.mock_cursor.rowcount = 0
    
        response = self.client.delete('/api/product_categories/9999')  # Use an invalid category_id
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'Category not found', response.data)

        # Test for invalid input (empty category_id) when deleting a category (DELETE)
        response = self.client.delete('/api/product_categories/', json={})  # Missing category_id
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.', response.data)
        
    @patch("app.app.create_connection")
    def test_create_product(self, mock_create_connection):
        # Mock database connection and cursor
        mock_create_connection.return_value = self.mock_connection
        self.mock_connection.cursor.return_value = self.mock_cursor
        self.mock_cursor.lastrowid = 1  # Simulate a fixed product_id for the created product

        # Mock data input
        mock_data = {
            "product_name": "New Product",
            "description": "A brand new product",
            "quantity_in_stock": 150,
            "unit_price": 29.99,
            "category_id": 1,
            "reorder_level": 5
        }

        # Call the endpoint
        response = self.client.post("/api/products", json=mock_data)

        # Assertions
        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.json,
            {"message": "Product created successfully.", "product_id": 1}
        )
        self.mock_cursor.execute.assert_called_with(
            """
            INSERT INTO Products (product_name, description, quantity_in_stock, unit_price, category_id, reorder_level)
            VALUES (%s, %s, %s, %s, %s, %s);
            """,
            ("New Product", "A brand new product", 150, 29.99, 1, 5)
        )

    @patch("app.app.create_connection")
    def test_get_all_products(self, mock_create_connection):
        # Mock database connection and cursor
        mock_create_connection.return_value = self.mock_connection
        self.mock_connection.cursor.return_value = self.mock_cursor
        self.mock_cursor.fetchall.return_value = [
            {
                "product_id": 1,
                "product_name": "Test Product 1",
                "description": "A test product",
                "quantity_in_stock": 100,
                "unit_price": 19.99,
                "category_id": 1,
                "reorder_level": 5
            },
            {
                "product_id": 2,
                "product_name": "Test Product 2",
                "description": "Another test product",
                "quantity_in_stock": 50,
                "unit_price": 9.99,
                "category_id": 2,
                "reorder_level": 10
            }
        ]
        
        # Call the endpoint
        response = self.client.get("/api/products")
        
        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 2)  # Ensure two products are returned
        self.mock_cursor.execute.assert_called_with("SELECT * FROM Products;")

    @patch("app.app.create_connection")
    def test_get_single_product(self, mock_create_connection):
        # Mock database connection and cursor
        mock_create_connection.return_value = self.mock_connection
        self.mock_connection.cursor.return_value = self.mock_cursor
        self.mock_cursor.fetchone.return_value = {
            "product_id": 1,
            "product_name": "Test Product",
            "description": "A test product",
            "quantity_in_stock": 100,
            "unit_price": 19.99,
            "category_id": 1,
            "reorder_level": 5
        }

        # Call the endpoint
        response = self.client.get("/api/products/1")

        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json,
            {
                "product_id": 1,
                "product_name": "Test Product",
                "description": "A test product",
                "quantity_in_stock": 100,
                "unit_price": 19.99,
                "category_id": 1,
                "reorder_level": 5
            }
        )
        self.mock_cursor.execute.assert_called_with(
            "SELECT * FROM Products WHERE product_id = %s;", (1,)
        )

    @patch("app.app.create_connection")
    def test_update_product(self, mock_create_connection):
        # Mock database connection and cursor
        mock_create_connection.return_value = self.mock_connection
        self.mock_connection.cursor.return_value = self.mock_cursor
        self.mock_cursor.rowcount = 1  # Simulate a successful update
        
        # Mock data input
        mock_data = {
            "product_name": "Updated Product",
            "description": "Updated product description",
            "quantity_in_stock": 120,
            "unit_price": 24.99,
            "category_id": 1,
            "reorder_level": 8
        }
        
        # Call the endpoint
        response = self.client.put("/api/products/1", json=mock_data)
        
        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json,
            {"message": "Product updated successfully."}
        )
        self.mock_cursor.execute.assert_called_with(
            """
            UPDATE Products
            SET product_name = %s, description = %s, quantity_in_stock = %s, unit_price = %s, category_id = %s, reorder_level = %s
            WHERE product_id = %s;
            """,
            ("Updated Product", "Updated product description", 120, 24.99, 1, 8, 1)
        )

    @patch("app.app.create_connection")
    def test_delete_product(self, mock_create_connection):
        # Mock database connection and cursor
        mock_create_connection.return_value = self.mock_connection
        self.mock_connection.cursor.return_value = self.mock_cursor
        self.mock_cursor.rowcount = 1  # Simulate a successful delete
        
        # Call the endpoint
        response = self.client.delete("/api/products/1")
        
        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json,
            {"message": "Product deleted successfully."}
        )
        self.mock_cursor.execute.assert_called_with(
            "DELETE FROM Products WHERE product_id = %s;", (1,)
        )
        
    @patch("app.app.create_connection")  # Updated patch path to app.app.create_connection
    def test_create_product_invalid_input(self, mock_create_connection):
        # Mock database connection and cursor
        mock_create_connection.return_value = self.mock_connection
        self.mock_connection.cursor.return_value = self.mock_cursor

        # Test missing required fields (POST)
        mock_data = {
            'unit_price': 15.99,  # Missing product_name, category_id, and reorder_level
            'description': 'A new book',
            'quantity_in_stock': 100
        }
        response = self.client.post('/api/products', json=mock_data)
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Missing required fields', response.data)

    @patch("app.app.create_connection")  # Updated patch path to app.app.create_connection
    def test_get_product_invalid(self, mock_create_connection):
       # Mock database connection and cursor
        mock_create_connection.return_value = self.mock_connection
        self.mock_connection.cursor.return_value = self.mock_cursor
    
        # Simulate product not found
        self.mock_cursor.fetchone.return_value = None

        # Test for nonexistent product (GET)
        response = self.client.get('/api/products/9999')  # Use an invalid product_id
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'Product not found', response.data)

    @patch("app.app.create_connection")  # Updated patch path to app.app.create_connection
    def test_update_product_invalid_input(self, mock_create_connection):
        # Mock database connection and cursor
        mock_create_connection.return_value = self.mock_connection
        self.mock_connection.cursor.return_value = self.mock_cursor
    
        # Test for updating a nonexistent product (PUT)
        mock_data = {
            'product_name': 'Updated Product',
            'description': 'Updated description',
            'quantity_in_stock': 150,
            'unit_price': 20.99,
            'category_id': 2,
            'reorder_level': 10
        }
    
        # Simulate no rows affected (nonexistent product)
        self.mock_cursor.rowcount = 0
    
        response = self.client.put('/api/products/9999', json=mock_data)  # Use an invalid product_id
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'Product not found', response.data)

        # Test for invalid input (empty product_id) when updating a product (PUT)
        mock_data = {
            'product_name': 'Updated Product',
            'description': 'Updated description',
            'quantity_in_stock': 150,
            'unit_price': 20.99,
            'category_id': 2,
            'reorder_level': 10
        }
        response = self.client.put('/api/products/', json=mock_data)  # Missing product_id
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.', response.data)

    @patch("app.app.create_connection")  # Updated patch path to app.app.create_connection
    def test_delete_product_invalid(self, mock_create_connection):
        # Mock database connection and cursor
        mock_create_connection.return_value = self.mock_connection
        self.mock_connection.cursor.return_value = self.mock_cursor
    
        # Test for deleting a nonexistent product (DELETE)
        self.mock_cursor.rowcount = 0
    
        response = self.client.delete('/api/products/9999')  # Use an invalid product_id
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'Product not found', response.data)

        # Test for invalid input (empty product_id) when deleting a product (DELETE)
        response = self.client.delete('/api/products/', json={})  # Missing product_id
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.', response.data)
        
    @patch("app.app.create_connection")
    def test_create_order(self, mock_create_connection):
        # Mock database connection and cursor
        mock_create_connection.return_value = self.mock_connection
        self.mock_connection.cursor.return_value = self.mock_cursor
        self.mock_cursor.lastrowid = 1  # Simulate a fixed order_id for the created order

        # Mock data input
        mock_data = {
            "customer_id": 123,
            "status": "Pending",
            "total_amount": 99.99,
            "payment_status": "Unpaid",
            "shipping_address": "123 Example St, City, Country"
        }

        # Call the endpoint
        response = self.client.post("/api/orders", json=mock_data)

        # Assertions
        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.json,
            {"message": "Order created successfully.", "order_id": 1}
        )
        self.mock_cursor.execute.assert_called_with(
            """
            INSERT INTO Orders (customer_id, status, total_amount, payment_status, shipping_address)
            VALUES (%s, %s, %s, %s, %s);
            """,
            (123, "Pending", 99.99, "Unpaid", "123 Example St, City, Country")
        )

    @patch("app.app.create_connection")
    def test_get_all_orders(self, mock_create_connection):
        # Mock database connection and cursor
        mock_create_connection.return_value = self.mock_connection
        self.mock_connection.cursor.return_value = self.mock_cursor
        self.mock_cursor.fetchall.return_value = [
            {
                "order_id": 1,
                "customer_id": 123,
                "status": "Pending",
                "total_amount": 99.99,
                "payment_status": "Unpaid",
                "shipping_address": "123 Example St, City, Country"
            },
            {
                "order_id": 2,
                "customer_id": 456,
                "status": "Shipped",
                "total_amount": 149.99,
                "payment_status": "Paid",
                "shipping_address": "456 Another St, City, Country"
            }
        ]
        
        # Call the endpoint
        response = self.client.get("/api/orders")
        
        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 2)  # Ensure two orders are returned
        self.mock_cursor.execute.assert_called_with("SELECT * FROM Orders;")

    @patch("app.app.create_connection")
    def test_get_single_order(self, mock_create_connection):
        # Mock database connection and cursor
        mock_create_connection.return_value = self.mock_connection
        self.mock_connection.cursor.return_value = self.mock_cursor
        self.mock_cursor.fetchone.return_value = {
            "order_id": 1,
            "customer_id": 123,
            "status": "Pending",
            "total_amount": 99.99,
            "payment_status": "Unpaid",
            "shipping_address": "123 Example St, City, Country"
        }

        # Call the endpoint
        response = self.client.get("/api/orders/1")

        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json,
            {
                "order_id": 1,
                "customer_id": 123,
                "status": "Pending",
                "total_amount": 99.99,
                "payment_status": "Unpaid",
                "shipping_address": "123 Example St, City, Country"
            }
        )
        self.mock_cursor.execute.assert_called_with(
            "SELECT * FROM Orders WHERE order_id = %s;", (1,)
        )

    @patch("app.app.create_connection")
    def test_update_order(self, mock_create_connection):
        # Mock database connection and cursor
        mock_create_connection.return_value = self.mock_connection
        self.mock_connection.cursor.return_value = self.mock_cursor
        self.mock_cursor.rowcount = 1  # Simulate a successful update
        
        # Mock data input
        mock_data = {
            "customer_id": 123,
            "status": "Shipped",
            "total_amount": 99.99,
            "payment_status": "Paid",
            "shipping_address": "123 Updated St, City, Country"
        }
        
        # Call the endpoint
        response = self.client.put("/api/orders/1", json=mock_data)
        
        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json,
            {"message": "Order updated successfully."}
        )
        self.mock_cursor.execute.assert_called_with(
            """
            UPDATE Orders
            SET customer_id = %s, status = %s, total_amount = %s, payment_status = %s, shipping_address = %s
            WHERE order_id = %s;
            """,
            (123, "Shipped", 99.99, "Paid", "123 Updated St, City, Country", 1)
        )

    @patch("app.app.create_connection")
    def test_delete_order(self, mock_create_connection):
        # Mock database connection and cursor
        mock_create_connection.return_value = self.mock_connection
        self.mock_connection.cursor.return_value = self.mock_cursor
        self.mock_cursor.rowcount = 1  # Simulate a successful delete
        
        # Call the endpoint
        response = self.client.delete("/api/orders/1")
        
        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json,
            {"message": "Order deleted successfully."}
        )
        self.mock_cursor.execute.assert_called_with(
            "DELETE FROM Orders WHERE order_id = %s;", (1,)
        )
        
    @patch("app.app.create_connection")  # Updated patch path to app.app.create_connection
    def test_create_order_invalid_input(self, mock_create_connection):
        # Mock database connection and cursor
        mock_create_connection.return_value = self.mock_connection
        self.mock_connection.cursor.return_value = self.mock_cursor

        # Test missing required fields (POST)
        mock_data = {
            'status': 'pending',
            'total_amount': 100.50,
            'payment_status': 'unpaid',
            'shipping_address': '123 Street, City, Country'  # Missing customer_id
        }
        response = self.client.post('/api/orders', json=mock_data)
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Missing required fields', response.data)

    @patch("app.app.create_connection")  # Updated patch path to app.app.create_connection
    def test_get_order_invalid(self, mock_create_connection):
        # Mock database connection and cursor
        mock_create_connection.return_value = self.mock_connection
        self.mock_connection.cursor.return_value = self.mock_cursor
    
        # Simulate order not found
        self.mock_cursor.fetchone.return_value = None

        # Test for nonexistent order (GET)
        response = self.client.get('/api/orders/9999')  # Use an invalid order_id
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'Order not found', response.data)

    @patch("app.app.create_connection")  # Updated patch path to app.app.create_connection
    def test_update_order_invalid_input(self, mock_create_connection):
        # Mock database connection and cursor
        mock_create_connection.return_value = self.mock_connection
        self.mock_connection.cursor.return_value = self.mock_cursor
    
        # Test for updating a nonexistent order (PUT)
        mock_data = {
            'customer_id': 1,
            'status': 'shipped',
            'total_amount': 200.00,
            'payment_status': 'paid',
            'shipping_address': '456 Avenue, City, Country'
        }
    
        # Simulate no rows affected (nonexistent order)
        self.mock_cursor.rowcount = 0
    
        response = self.client.put('/api/orders/9999', json=mock_data)  # Use an invalid order_id
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'Order not found', response.data)

        # Test for invalid input (empty order_id) when updating an order (PUT)
        mock_data = {
            'customer_id': 1,
            'status': 'shipped',
            'total_amount': 200.00,
            'payment_status': 'paid',
            'shipping_address': '456 Avenue, City, Country'
        }
        response = self.client.put('/api/orders/', json=mock_data)  # Missing order_id
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.', response.data)

    @patch("app.app.create_connection")  # Updated patch path to app.app.create_connection
    def test_delete_order_invalid(self, mock_create_connection):
        # Mock database connection and cursor
        mock_create_connection.return_value = self.mock_connection
        self.mock_connection.cursor.return_value = self.mock_cursor
    
        # Test for deleting a nonexistent order (DELETE)
        self.mock_cursor.rowcount = 0
    
        response = self.client.delete('/api/orders/9999')  # Use an invalid order_id
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'Order not found', response.data)

        # Test for invalid input (empty order_id) when deleting an order (DELETE)
        response = self.client.delete('/api/orders/', json={})  # Missing order_id
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.', response.data)

        
    @patch("app.app.create_connection")  # Updated patch path to app.app.create_connection
    def test_create_order_item(self, mock_create_connection):
        # Mock database connection and cursor
        mock_create_connection.return_value = self.mock_connection
        self.mock_connection.cursor.return_value = self.mock_cursor
        self.mock_cursor.lastrowid = 1  # Simulate a fixed order_item_id for the created order item

        # Mock data input
        mock_data = {
            'order_id': 1,
            'product_id': 1,
            'quantity': 5,
            'unit_price': 10.0
        }

        # Call the endpoint
        response = self.client.post('/api/order_items', json=mock_data)

        # Assertions
        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.json,
            {'message': 'Order item created successfully.', 'order_item_id': 1}
        )
        self.mock_cursor.execute.assert_called_with(
            """
            INSERT INTO Order_Items (order_id, product_id, quantity, unit_price)
            VALUES (%s, %s, %s, %s);
            """,
            (1, 1, 5, 10.0)
        )

    @patch("app.app.create_connection")  # Updated patch path to app.app.create_connection
    def test_get_all_order_items(self, mock_create_connection):
        # Mock database connection and cursor
        mock_create_connection.return_value = self.mock_connection
        self.mock_connection.cursor.return_value = self.mock_cursor
        self.mock_cursor.fetchall.return_value = [
            {'order_item_id': 1, 'order_id': 1, 'product_id': 1, 'quantity': 5, 'unit_price': 10.0}
        ]
        
        # Call the endpoint
        response = self.client.get('/api/order_items')
        
        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json,
            [{'order_item_id': 1, 'order_id': 1, 'product_id': 1, 'quantity': 5, 'unit_price': 10.0}]
        )
        self.mock_cursor.execute.assert_called_with('SELECT * FROM Order_Items;')

    @patch("app.app.create_connection")  # Updated patch path to app.app.create_connection
    def test_get_single_order_item(self, mock_create_connection):
        # Mock database connection and cursor
        mock_create_connection.return_value = self.mock_connection
        self.mock_connection.cursor.return_value = self.mock_cursor
        self.mock_cursor.fetchone.return_value = {
            'order_item_id': 1, 'order_id': 1, 'product_id': 1, 'quantity': 5, 'unit_price': 10.0
        }

        # Call the endpoint
        response = self.client.get('/api/order_items/1')

        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json,
            {'order_item_id': 1, 'order_id': 1, 'product_id': 1, 'quantity': 5, 'unit_price': 10.0}
        )
        self.mock_cursor.execute.assert_called_with('SELECT * FROM Order_Items WHERE order_item_id = %s;', (1,))

    @patch("app.app.create_connection")  # Updated patch path to app.app.create_connection
    def test_update_order_item(self, mock_create_connection):
        # Mock database connection and cursor
        mock_create_connection.return_value = self.mock_connection
        self.mock_connection.cursor.return_value = self.mock_cursor
        self.mock_cursor.rowcount = 1  # Simulate a successful update
        
        # Mock data input
        mock_data = {
            'order_id': 1,
            'product_id': 1,
            'quantity': 10,
            'unit_price': 12.0
        }
        
        # Call the endpoint
        response = self.client.put('/api/order_items/1', json=mock_data)
        
        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json,
            {'message': 'Order item updated successfully.'}
        )
        self.mock_cursor.execute.assert_called_with(
            """
            UPDATE Order_Items
            SET order_id = %s, product_id = %s, quantity = %s, unit_price = %s
            WHERE order_item_id = %s;
            """,
            (1, 1, 10, 12.0, 1)
        )

    @patch("app.app.create_connection")  # Updated patch path to app.app.create_connection
    def test_delete_order_item(self, mock_create_connection):
        # Mock database connection and cursor
        mock_create_connection.return_value = self.mock_connection
        self.mock_connection.cursor.return_value = self.mock_cursor
        self.mock_cursor.rowcount = 1  # Simulate a successful delete
        
        # Call the endpoint
        response = self.client.delete('/api/order_items/1')
        
        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json,
            {'message': 'Order item deleted successfully.'}
        )
        self.mock_cursor.execute.assert_called_with(
            'DELETE FROM Order_Items WHERE order_item_id = %s;', (1,)
        )
    @patch("app.app.create_connection")  # Updated patch path to app.app.create_connection
    def test_create_order_item_invalid_input(self, mock_create_connection):
        # Mock database connection and cursor
        mock_create_connection.return_value = self.mock_connection
        self.mock_connection.cursor.return_value = self.mock_cursor

        # Test missing required fields (POST)
        mock_data = {
            'order_id': 1,
            'quantity': 10  # Missing product_id and unit_price
        }
        response = self.client.post('/api/order_items', json=mock_data)
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Missing required fields', response.data)

    @patch("app.app.create_connection")  # Updated patch path to app.app.create_connection
    def test_get_order_item_invalid(self, mock_create_connection):
        # Mock database connection and cursor
        mock_create_connection.return_value = self.mock_connection
        self.mock_connection.cursor.return_value = self.mock_cursor

        # Simulate order item not found
        self.mock_cursor.fetchone.return_value = None

        # Test for nonexistent order item (GET)
        response = self.client.get('/api/order_items/9999')  # Use an invalid order_item_id
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'Order item not found', response.data)

    @patch("app.app.create_connection")  # Updated patch path to app.app.create_connection
    def test_update_order_item_invalid_input(self, mock_create_connection):
        # Mock database connection and cursor
        mock_create_connection.return_value = self.mock_connection
        self.mock_connection.cursor.return_value = self.mock_cursor

        # Test for updating a nonexistent order item (PUT)
        mock_data = {
            'order_id': 1,
            'product_id': 2,
            'quantity': 5,
            'unit_price': 15.0
        }

        # Simulate no rows affected (nonexistent order item)
        self.mock_cursor.rowcount = 0

        response = self.client.put('/api/order_items/9999', json=mock_data)  # Use an invalid order_item_id
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'Order item not found', response.data)

        # Test for invalid input (missing order_item_id) when updating an order item (PUT)
        response = self.client.put('/api/order_items/', json=mock_data)  # Missing order_item_id
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'The requested URL was not found on the server.', response.data)

    @patch("app.app.create_connection")  # Updated patch path to app.app.create_connection
    def test_delete_order_item_invalid(self, mock_create_connection):
        # Mock database connection and cursor
        mock_create_connection.return_value = self.mock_connection
        self.mock_connection.cursor.return_value = self.mock_cursor

        # Test for deleting a nonexistent order item (DELETE)
        self.mock_cursor.rowcount = 0

        response = self.client.delete('/api/order_items/9999')  # Use an invalid order_item_id
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'Order item not found', response.data)

        # Test for invalid input (missing order_item_id) when deleting an order item (DELETE)
        response = self.client.delete('/api/order_items/', json={})  # Missing order_item_id
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'The requested URL was not found on the server.', response.data)
   
    @patch("app.app.create_connection")  # Updated patch path to app.app.create_connection
    def test_create_report(self, mock_create_connection):
        # Mock database connection and cursor
        mock_create_connection.return_value = self.mock_connection
        self.mock_connection.cursor.return_value = self.mock_cursor
        self.mock_cursor.lastrowid = 1  # Simulate a fixed report_id for the created report

        # Mock data input
        mock_data = {
            'report_type': 'Sales',
            'user_id': 1,
            'report_data': 'Some sales data'
        }

        # Call the endpoint
        response = self.client.post('/api/reports', json=mock_data)

        # Assertions
        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.json,
            {'message': 'Report created successfully.', 'report_id': 1}
        )
        self.mock_cursor.execute.assert_called_with(
            """
            INSERT INTO Reports (report_type, user_id, report_data)
            VALUES (%s, %s, %s);
            """,
            ('Sales', 1, 'Some sales data')
        )

    @patch("app.app.create_connection")  # Updated patch path to app.app.create_connection
    def test_get_all_reports(self, mock_create_connection):
        # Mock database connection and cursor
        mock_create_connection.return_value = self.mock_connection
        self.mock_connection.cursor.return_value = self.mock_cursor
        self.mock_cursor.fetchall.return_value = [
            {'report_id': 1, 'report_type': 'Sales', 'user_id': 1, 'report_data': 'Some sales data'}
        ]
        
        # Call the endpoint
        response = self.client.get('/api/reports')
        
        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json,
            [{'report_id': 1, 'report_type': 'Sales', 'user_id': 1, 'report_data': 'Some sales data'}]
        )
        self.mock_cursor.execute.assert_called_with('SELECT * FROM Reports;')

    @patch("app.app.create_connection")  # Updated patch path to app.app.create_connection
    def test_get_single_report(self, mock_create_connection):
        # Mock database connection and cursor
        mock_create_connection.return_value = self.mock_connection
        self.mock_connection.cursor.return_value = self.mock_cursor
        self.mock_cursor.fetchone.return_value = {
            'report_id': 1, 'report_type': 'Sales', 'user_id': 1, 'report_data': 'Some sales data'
        }

        # Call the endpoint
        response = self.client.get('/api/reports/1')

        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json,
            {'report_id': 1, 'report_type': 'Sales', 'user_id': 1, 'report_data': 'Some sales data'}
        )
        self.mock_cursor.execute.assert_called_with('SELECT * FROM Reports WHERE report_id = %s;', (1,))

    @patch("app.app.create_connection")  # Updated patch path to app.app.create_connection
    def test_update_report(self, mock_create_connection):
        # Mock database connection and cursor
        mock_create_connection.return_value = self.mock_connection
        self.mock_connection.cursor.return_value = self.mock_cursor
        self.mock_cursor.rowcount = 1  # Simulate a successful update
        
        # Mock data input
        mock_data = {
            'report_type': 'Inventory',
            'user_id': 2,
            'report_data': 'Some inventory data'
        }
        
        # Call the endpoint
        response = self.client.put('/api/reports/1', json=mock_data)
        
        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json,
            {'message': 'Report updated successfully.'}
        )
        self.mock_cursor.execute.assert_called_with(
            """
            UPDATE Reports
            SET report_type = %s, user_id = %s, report_data = %s
            WHERE report_id = %s;
            """,
            ('Inventory', 2, 'Some inventory data', 1)
        )

    @patch("app.app.create_connection")  # Updated patch path to app.app.create_connection
    def test_delete_report(self, mock_create_connection):
        # Mock database connection and cursor
        mock_create_connection.return_value = self.mock_connection
        self.mock_connection.cursor.return_value = self.mock_cursor
        self.mock_cursor.rowcount = 1  # Simulate a successful delete
        
        # Call the endpoint
        response = self.client.delete('/api/reports/1')
        
        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json,
            {'message': 'Report deleted successfully.'}
        )
        self.mock_cursor.execute.assert_called_with(
            'DELETE FROM Reports WHERE report_id = %s;', (1,)
        )
        
    @patch("app.app.create_connection")  # Updated patch path to app.app.create_connection
    def test_create_report_invalid_input(self, mock_create_connection):
        # Mock database connection and cursor
        mock_create_connection.return_value = self.mock_connection
        self.mock_connection.cursor.return_value = self.mock_cursor

        # Test missing required fields (POST)
        mock_data = {
            'user_id': 1,
            'report_data': 'Some data'  # Missing report_type
        }
        response = self.client.post('/api/reports', json=mock_data)
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Missing required fields', response.data)

    @patch("app.app.create_connection")  # Updated patch path to app.app.create_connection
    def test_get_report_invalid(self, mock_create_connection):
        # Mock database connection and cursor
        mock_create_connection.return_value = self.mock_connection
        self.mock_connection.cursor.return_value = self.mock_cursor

        # Simulate report not found
        self.mock_cursor.fetchone.return_value = None

        # Test for nonexistent report (GET)
        response = self.client.get('/api/reports/9999')  # Use an invalid report_id
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'Report not found', response.data)

    @patch("app.app.create_connection")  # Updated patch path to app.app.create_connection
    def test_update_report_invalid_input(self, mock_create_connection):
        # Mock database connection and cursor
        mock_create_connection.return_value = self.mock_connection
        self.mock_connection.cursor.return_value = self.mock_cursor

        # Test for updating a nonexistent report (PUT)
        mock_data = {
            'report_type': 'Error',
            'user_id': 1,
            'report_data': 'Updated data'
        }

        # Simulate no rows affected (nonexistent report)
        self.mock_cursor.rowcount = 0

        response = self.client.put('/api/reports/9999', json=mock_data)  # Use an invalid report_id
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'Report not found', response.data)

        # Test for invalid input (empty report_id) when updating a report (PUT)
        response = self.client.put('/api/reports/', json=mock_data)  # Missing report_id
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.', response.data)

    @patch("app.app.create_connection")  # Updated patch path to app.app.create_connection
    def test_delete_report_invalid(self, mock_create_connection):
        # Mock database connection and cursor
        mock_create_connection.return_value = self.mock_connection
        self.mock_connection.cursor.return_value = self.mock_cursor

        # Test for deleting a nonexistent report (DELETE)
        self.mock_cursor.rowcount = 0

        response = self.client.delete('/api/reports/9999')  # Use an invalid report_id
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'Report not found', response.data)

        # Test for invalid input (empty report_id) when deleting a report (DELETE)
        response = self.client.delete('/api/reports/', json={})  # Missing report_id
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.', response.data)


if __name__ == "__main__":
    unittest.main()
