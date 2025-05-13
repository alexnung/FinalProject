import sys
from pathlib import Path
import unittest
from unittest.mock import patch, MagicMock
from io import StringIO

# Dynamically add the `app` folder to the Python path
parent_dir = Path(__file__).resolve().parent.parent  # Go up one folder
app_dir = parent_dir / "app"
sys.path.append(str(app_dir))

import mysql_connect

class TestMySQLConnect(unittest.TestCase):

    @patch("mysql_connect.get_connection")
    def test_successful_connection(self, mock_get_connection):
        """
        Test if the connection function works successfully.
        """
        mock_connection = MagicMock()
        mock_connection.is_connected.return_value = True
        mock_get_connection.return_value = mock_connection

        # Call the function
        connection = mysql_connect.get_connection()

        # Assertions
        self.assertIsNotNone(connection)
        self.assertTrue(connection.is_connected())

    @patch("mysql_connect.get_connection")
    @patch("sys.stdout", new_callable=StringIO)  # Capture print statements
    def test_failed_connection(self, mock_stdout, mock_get_connection):
        """
        Test if the function handles a failed connection properly.
        """
        # Simulate an exception (like a failed database connection)
        mock_get_connection.side_effect = Exception("Connection failed")

        # Call the function and check that the exception is raised
        with self.assertRaises(Exception):  # Ensure the exception is raised
            try:
                mysql_connect.get_connection()
            except Exception as e:
                # Capture the output during exception handling
                print(f"Error connecting to MySQL: {e}")
                raise

        # Check that the expected error message is printed
        output = mock_stdout.getvalue()
        self.assertIn("Error connecting to MySQL:", output)
        self.assertIn("Connection failed", output)

if __name__ == "__main__":
    unittest.main()
