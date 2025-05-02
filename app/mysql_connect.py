import mysql.connector
from mysql.connector import Error

def create_connection(host, user, password, database):
    """
    Create a connection to the MySQL database.
    
    Parameters:
        host (str): The hostname or IP address of the MySQL server.
        user (str): The MySQL username.
        password (str): The MySQL user's password.
        database (str): The name of the database to connect to.

    Returns:
        connection: A MySQL connection object or None if connection fails.
    """
    try:
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        if connection.is_connected():
            print("Connection successful!")
            return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

def close_connection(connection):
    """
    Close the MySQL database connection.

    Parameters:
        connection: The MySQL connection object.
    """
    if connection and connection.is_connected():
        connection.close()
        print("Connection closed.")

# Example Usage
if __name__ == "__main__":
    # Connection parameters
    host = "localhost"        # Replace with your MySQL server host
    user = "root"             # Replace with your MySQL username
    password = "root"         # Replace with your MySQL password
    database = "inventorymanagement"  # Replace with your database name

    # Create a connection
    connection = create_connection(host, user, password, database)

    # Perform some optional operations
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            record = cursor.fetchone()
            print("Connected to database:", record)
        except Error as e:
            print("Error during query execution:", e)
        finally:
            # Close the connection
            close_connection(connection)
