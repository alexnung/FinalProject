from flask import Flask, jsonify, request
import mysql.connector
from mysql.connector import Error
from flask_cors import CORS,cross_origin

app = Flask(__name__)

CORS(app)

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
@cross_origin()
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
@app.route('/api/product_categories', methods=['GET', 'POST', 'PUT', 'DELETE'])
@cross_origin()
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
@cross_origin()
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

# 4. Orders Table
@app.route('/api/orders', methods=['GET', 'POST', 'PUT', 'DELETE'])
@cross_origin()
def manage_orders():
    connection = create_connection()
    if not connection:
        return error_response("Database connection failed.")
    try:
        cursor = connection.cursor(dictionary=True)
        if request.method == 'GET':
            cursor.execute("SELECT * FROM Orders;")
            return jsonify(cursor.fetchall())
        elif request.method == 'POST':
            data = request.get_json()
            required_fields = ['customer_id', 'status', 'total_amount', 'payment_status', 'shipping_address']
            if not validate_data(data, required_fields):
                return error_response("Missing required fields.")
            query = """
            INSERT INTO Orders (customer_id, status, total_amount, payment_status, shipping_address)
            VALUES (%s, %s, %s, %s, %s);
            """
            cursor.execute(query, (
                data['customer_id'], data['status'], data['total_amount'],
                data['payment_status'], data['shipping_address']
            ))
            connection.commit()
            return jsonify({'message': 'Order created successfully.', 'order_id': cursor.lastrowid}), 201
        elif request.method == 'PUT':
            data = request.get_json()
            order_id = data.get('order_id')
            if not order_id:
                return error_response("Order ID is required for updating.")
            query = """
            UPDATE Orders
            SET customer_id = %s, status = %s, total_amount = %s, payment_status = %s, shipping_address = %s
            WHERE order_id = %s;
            """
            cursor.execute(query, (
                data['customer_id'], data['status'], data['total_amount'],
                data['payment_status'], data['shipping_address'], order_id
            ))
            connection.commit()
            if cursor.rowcount == 0:
                return error_response("Order not found.", 404)
            return jsonify({'message': 'Order updated successfully.'})
        elif request.method == 'DELETE':
            order_id = request.args.get('order_id')
            if not order_id:
                return error_response("Order ID is required for deletion.")
            query = "DELETE FROM Orders WHERE order_id = %s;"
            cursor.execute(query, (order_id,))
            connection.commit()
            if cursor.rowcount == 0:
                return error_response("Order not found.", 404)
            return jsonify({'message': 'Order deleted successfully.'})
    except Error as e:
        return error_response(f"Error managing orders: {str(e)}")
    finally:
        connection.close()

# 5. Order_Items Table
@app.route('/api/order_items', methods=['GET', 'POST', 'PUT', 'DELETE'])
@cross_origin()
def manage_order_items():
    connection = create_connection()
    if not connection:
        return error_response("Database connection failed.")
    try:
        cursor = connection.cursor(dictionary=True)
        if request.method == 'GET':
            cursor.execute("SELECT * FROM Order_Items;")
            return jsonify(cursor.fetchall())
        elif request.method == 'POST':
            data = request.get_json()
            required_fields = ['order_id', 'product_id', 'quantity', 'unit_price']
            if not validate_data(data, required_fields):
                return error_response("Missing required fields.")
            query = """
            INSERT INTO Order_Items (order_id, product_id, quantity, unit_price)
            VALUES (%s, %s, %s, %s);
            """
            cursor.execute(query, (
                data['order_id'], data['product_id'], data['quantity'], data['unit_price']
            ))
            connection.commit()
            return jsonify({'message': 'Order item created successfully.', 'order_item_id': cursor.lastrowid}), 201
        elif request.method == 'PUT':
            data = request.get_json()
            order_item_id = data.get('order_item_id')
            if not order_item_id:
                return error_response("Order item ID is required for updating.")
            query = """
            UPDATE Order_Items
            SET order_id = %s, product_id = %s, quantity = %s, unit_price = %s
            WHERE order_item_id = %s;
            """
            cursor.execute(query, (
                data['order_id'], data['product_id'], data['quantity'],
                data['unit_price'], order_item_id
            ))
            connection.commit()
            if cursor.rowcount == 0:
                return error_response("Order item not found.", 404)
            return jsonify({'message': 'Order item updated successfully.'})
        elif request.method == 'DELETE':
            order_item_id = request.args.get('order_item_id')
            if not order_item_id:
                return error_response("Order item ID is required for deletion.")
            query = "DELETE FROM Order_Items WHERE order_item_id = %s;"
            cursor.execute(query, (order_item_id,))
            connection.commit()
            if cursor.rowcount == 0:
                return error_response("Order item not found.", 404)
            return jsonify({'message': 'Order item deleted successfully.'})
    except Error as e:
        return error_response(f"Error managing order items: {str(e)}")
    finally:
        connection.close()

# 7. Reports Table
@app.route('/api/reports', methods=['GET', 'POST', 'PUT', 'DELETE'])
@cross_origin()
def manage_reports():
    connection = create_connection()
    if not connection:
        return error_response("Database connection failed.")
    try:
        cursor = connection.cursor(dictionary=True)
        if request.method == 'GET':
            cursor.execute("SELECT * FROM Reports;")
            return jsonify(cursor.fetchall())
        elif request.method == 'POST':
            data = request.get_json()
            required_fields = ['report_type', 'user_id', 'report_data']
            if not validate_data(data, required_fields):
                return error_response("Missing required fields.")
            query = """
            INSERT INTO Reports (report_type, user_id, report_data)
            VALUES (%s, %s, %s);
            """
            cursor.execute(query, (data['report_type'], data['user_id'], data['report_data']))
            connection.commit()
            return jsonify({'message': 'Report created successfully.', 'report_id': cursor.lastrowid}), 201
        elif request.method == 'PUT':
            data = request.get_json()
            report_id = data.get('report_id')
            if not report_id:
                return error_response("Report ID is required for updating.")
            query = """
            UPDATE Reports
            SET report_type = %s, user_id = %s, report_data = %s
            WHERE report_id = %s;
            """
            cursor.execute(query, (data['report_type'], data['user_id'], data['report_data'], report_id))
            connection.commit()
            if cursor.rowcount == 0:
                return error_response("Report not found.", 404)
            return jsonify({'message': 'Report updated successfully.'})
        elif request.method == 'DELETE':
            report_id = request.args.get('report_id')
            if not report_id:
                return error_response("Report ID is required for deletion.")
            query = "DELETE FROM Reports WHERE report_id = %s;"
            cursor.execute(query, (report_id,))
            connection.commit()
            if cursor.rowcount == 0:
                return error_response("Report not found.", 404)
            return jsonify({'message': 'Report deleted successfully.'})
    except Error as e:
        return error_response(f"Error managing reports: {str(e)}")
    finally:
        connection.close()

# 9. Invoices Table
@app.route('/api/invoices', methods=['GET', 'POST', 'PUT', 'DELETE'])
@cross_origin()
def manage_invoices():
    connection = create_connection()
    if not connection:
        return error_response("Database connection failed.")
    try:
        cursor = connection.cursor(dictionary=True)
        if request.method == 'GET':
            cursor.execute("SELECT * FROM Invoices;")
            return jsonify(cursor.fetchall())
        elif request.method == 'POST':
            data = request.get_json()
            required_fields = ['order_id', 'invoice_date', 'total_amount']
            if not validate_data(data, required_fields):
                return error_response("Missing required fields.")
            query = """
            INSERT INTO Invoices (order_id, invoice_date, total_amount, invoice_status, payment_due_date)
            VALUES (%s, %s, %s, %s, %s);
            """
            cursor.execute(query, (
                data['order_id'], data['invoice_date'], data['total_amount'], 
                data.get('invoice_status'), data.get('payment_due_date')
            ))
            connection.commit()
            return jsonify({'message': 'Invoice created successfully.', 'invoice_id': cursor.lastrowid}), 201
        elif request.method == 'PUT':
            data = request.get_json()
            invoice_id = data.get('invoice_id')
            if not invoice_id:
                return error_response("Invoice ID is required for updating.")
            query = """
            UPDATE Invoices
            SET order_id = %s, invoice_date = %s, total_amount = %s, invoice_status = %s, payment_due_date = %s
            WHERE invoice_id = %s;
            """
            cursor.execute(query, (
                data['order_id'], data['invoice_date'], data['total_amount'], 
                data.get('invoice_status'), data.get('payment_due_date'), invoice_id
            ))
            connection.commit()
            if cursor.rowcount == 0:
                return error_response("Invoice not found.", 404)
            return jsonify({'message': 'Invoice updated successfully.'})
        elif request.method == 'DELETE':
            invoice_id = request.args.get('invoice_id')
            if not invoice_id:
                return error_response("Invoice ID is required for deletion.")
            query = "DELETE FROM Invoices WHERE invoice_id = %s;"
            cursor.execute(query, (invoice_id,))
            connection.commit()
            if cursor.rowcount == 0:
                return error_response("Invoice not found.", 404)
            return jsonify({'message': 'Invoice deleted successfully.'})
    except Error as e:
        return error_response(f"Error managing invoices: {str(e)}")
    finally:
        connection.close()

if __name__ == '__main__':
    app.run(debug=False)
