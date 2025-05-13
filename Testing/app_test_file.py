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
    def test_get_users(self, mock_create_connection):
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

if __name__ == "__main__":
    unittest.main()
