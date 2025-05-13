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

        # Execute the code that uses get_connection
        try:
            # Use the reusable connection function
            connection = mysql_connect.get_connection()

            if connection and connection.is_connected():
                print("Connection successful!")
                print("Server info:", connection.server_info)

                # Perform a query to confirm the database connection
                cursor = connection.cursor()
                cursor.execute("SELECT DATABASE();")
                record = cursor.fetchone()
                print("You're connected to:", record)

                # Keep the connection open for further operations
                input("Press Enter to close the connection...")

                # Close the connection manually
                cursor.close()
                connection.close()
                print("Connection closed manually.")  # Confirming closure
        except Exception as e:
            print("An error occurred:", e)

        # Check that the expected error message is printed
        output = mock_stdout.getvalue()
        self.assertIn("An error occurred:", output)
        self.assertIn("Connection failed", output)

if __name__ == "__main__":
    unittest.main()
