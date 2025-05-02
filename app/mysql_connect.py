from db_util import get_connection

try:
    # Use the reusable connection function
    connection = get_connection()

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
