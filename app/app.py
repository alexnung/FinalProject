from flask import Flask, jsonify, request
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

# Utility function to create a database connection
def create_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="inventorymanagement"
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error connecting to database: {e}")
        return None

# Utility function for error response
def error_response(message, status_code=400):
    return jsonify({"error": message}), status_code

# Utility function to validate required data
def validate_data(data, required_fields):
    return all(field in data for field in required_fields)

### CRUD for Each Table ###

# 1. Users Table
@app.route('/api/users', methods=['GET', 'POST', 'PUT', 'DELETE'])
def manage_users():
    connection = create_connection()
    if not connection:
        return error_response("Database connection failed.")
    try:
        cursor = connection.cursor(dictionary=True)
        if request.method == 'GET':
            cursor.execute("SELECT * FROM Users;")
            return jsonify(cursor.fetchall())
        elif request.method == 'POST':
            data = request.get_json()
            required_fields = ['username', 'password_hash', 'role', 'email']
            if not validate_data(data, required_fields):
                return error_response("Missing required fields.")
            query = """
            INSERT INTO Users (username, password_hash, role, email, first_name, last_name)
            VALUES (%s, %s, %s, %s, %s, %s);
            """
            cursor.execute(query, (
                data['username'], data['password_hash'], data['role'], 
                data['email'], data.get('first_name'), data.get('last_name')
            ))
            connection.commit()
            return jsonify({'message': 'User created successfully.', 'user_id': cursor.lastrowid}), 201
        elif request.method == 'PUT':
            data = request.get_json()
            user_id = data.get('user_id')
            if not user_id:
                return error_response("User ID is required for updating.")
            query = """
            UPDATE Users
            SET username = %s, password_hash = %s, role = %s, email = %s, first_name = %s, last_name = %s
            WHERE user_id = %s;
            """
            cursor.execute(query, (
                data['username'], data['password_hash'], data['role'], 
                data['email'], data.get('first_name'), data.get('last_name'), user_id
            ))
            connection.commit()
            if cursor.rowcount == 0:
                return error_response("User not found.", 404)
            return jsonify({'message': 'User updated successfully.'})
        elif request.method == 'DELETE':
            user_id = request.args.get('user_id')
            if not user_id:
                return error_response("User ID is required for deletion.")
            query = "DELETE FROM Users WHERE user_id = %s;"
            cursor.execute(query, (user_id,))
            connection.commit()
            if cursor.rowcount == 0:
                return error_response("User not found.", 404)
            return jsonify({'message': 'User deleted successfully.'})
    except Error as e:
        return error_response(f"Error managing users: {str(e)}")
    finally:
        connection.close()

# 2. Product_Categories Table
@app.route('/api/categories', methods=['GET', 'POST', 'PUT', 'DELETE'])
def manage_categories():
    connection = create_connection()
    if not connection:
        return error_response("Database connection failed.")
    try:
        cursor = connection.cursor(dictionary=True)
        if request.method == 'GET':
            cursor.execute("SELECT * FROM Product_Categories;")
            return jsonify(cursor.fetchall())
        elif request.method == 'POST':
            data = request.get_json()
            required_fields = ['category_name']
            if not validate_data(data, required_fields):
                return error_response("Missing required fields.")
            query = """
            INSERT INTO Product_Categories (category_name, description)
            VALUES (%s, %s);
            """
            cursor.execute(query, (data['category_name'], data.get('description')))
            connection.commit()
            return jsonify({'message': 'Category created successfully.', 'category_id': cursor.lastrowid}), 201
        elif request.method == 'PUT':
            data = request.get_json()
            category_id = data.get('category_id')
            if not category_id:
                return error_response("Category ID is required for updating.")
            query = """
            UPDATE Product_Categories
            SET category_name = %s, description = %s
            WHERE category_id = %s;
            """
            cursor.execute(query, (data['category_name'], data.get('description'), category_id))
            connection.commit()
            if cursor.rowcount == 0:
                return error_response("Category not found.", 404)
            return jsonify({'message': 'Category updated successfully.'})
        elif request.method == 'DELETE':
            category_id = request.args.get('category_id')
            if not category_id:
                return error_response("Category ID is required for deletion.")
            query = "DELETE FROM Product_Categories WHERE category_id = %s;"
            cursor.execute(query, (category_id,))
            connection.commit()
            if cursor.rowcount == 0:
                return error_response("Category not found.", 404)
            return jsonify({'message': 'Category deleted successfully.'})
    except Error as e:
        return error_response(f"Error managing categories: {str(e)}")
    finally:
        connection.close()

# 3. Products Table
@app.route('/api/products', methods=['GET', 'POST', 'PUT', 'DELETE'])
def manage_products():
    connection = create_connection()
    if not connection:
        return error_response("Database connection failed.")
    try:
        cursor = connection.cursor(dictionary=True)
        if request.method == 'GET':
            cursor.execute("SELECT * FROM Products;")
            return jsonify(cursor.fetchall())
        elif request.method == 'POST':
            data = request.get_json()
            required_fields = ['product_name', 'unit_price', 'category_id']
            if not validate_data(data, required_fields):
                return error_response("Missing required fields.")
            query = """
            INSERT INTO Products (product_name, description, quantity_in_stock, unit_price, category_id)
            VALUES (%s, %s, %s, %s, %s);
            """
            cursor.execute(query, (
                data['product_name'], data.get('description'), data.get('quantity_in_stock', 0),
                data['unit_price'], data['category_id']
            ))
            connection.commit()
            return jsonify({'message': 'Product created successfully.', 'product_id': cursor.lastrowid}), 201
        elif request.method == 'PUT':
            data = request.get_json()
            product_id = data.get('product_id')
            if not product_id:
                return error_response("Product ID is required for updating.")
            query = """
            UPDATE Products
            SET product_name = %s, description = %s, quantity_in_stock = %s, unit_price = %s, category_id = %s
            WHERE product_id = %s;
            """
            cursor.execute(query, (
                data['product_name'], data.get('description'), data.get('quantity_in_stock'),
                data['unit_price'], data['category_id'], product_id
            ))
            connection.commit()
            if cursor.rowcount == 0:
                return error_response("Product not found.", 404)
            return jsonify({'message': 'Product updated successfully.'})
        elif request.method == 'DELETE':
            product_id = request.args.get('product_id')
            if not product_id:
                return error_response("Product ID is required for deletion.")
            query = "DELETE FROM Products WHERE product_id = %s;"
            cursor.execute(query, (product_id,))
            connection.commit()
            if cursor.rowcount == 0:
                return error_response("Product not found.", 404)
            return jsonify({'message': 'Product deleted successfully.'})
    except Error as e:
        return error_response(f"Error managing products: {str(e)}")
    finally:
        connection.close()

if __name__ == '__main__':
    app.run(debug=False)
