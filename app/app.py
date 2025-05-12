from flask import Flask, jsonify, request, session, render_template
from flask_login import LoginManager, login_required, UserMixin, login_user, logout_user
import mysql.connector
import json
import requests
from mysql.connector import Error
from flask_cors import CORS,cross_origin

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.secret_key = "your_secret_key"

CORS(
    app,
    supports_credentials=True,
    origins=["http://127.0.0.1:5000"],
    methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "http://127.0.0.1:5500"],
    allow_headers=["Content-Type", "Authorization"],
)

app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SECURE'] = False  # Set to True in production
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

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

# Define a simple User class
class User(UserMixin):
    def __init__(self, id):
        self.id = id

# User loader callback for loading user from the session
@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

# Dummy user authentication route (for testing purposes)
@app.route('/api/login', methods=['POST'])
@cross_origin()
def login():
    username = request.json.get("username")
    password = request.json.get("password")

    connection = create_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()

        if user and user['password'] == password:  # Ensure passwords are hashed in production!
            user_obj = User(id=user['username'])
            login_user(user_obj)
            
            # Store user information in the session
            session['user_id'] = user['username']
            
            # Create and return the response with the headers
            response = jsonify({"message": "Login successful!"})
            response.headers.add("Access-Control-Allow-Origin", request.headers.get("Origin"))
            response.headers.add("Access-Control-Allow-Credentials", "true")
            print(session)  # Debug session state
            return response, 200
        return jsonify({"message": "Invalid credentials!"}), 401
    return jsonify({"message": "Database connection failed!"}), 500

# Protected route that requires login
@app.route('/api/dashboard',)
@login_required
def dashboard():
    return render_template('dashboard.html')
    
@app.route('/api/orders',)
@login_required
def orders():
    return render_template('orders.html')
    
@app.route('/api/invoices',)
@login_required
def invoices():
    return render_template('invoices.html')    

import requests  # Import requests to fetch data from APIs

@app.route('/api/products')
@login_required
def products():
    try:
        # URLs for the APIs
        products_api_url = "http://127.0.0.1:5000/api/products"
        categories_api_url = "http://127.0.0.1:5000/api/product_categories"

        # Fetch data from APIs
        products_response = requests.get(products_api_url)
        categories_response = requests.get(categories_api_url)

        # Check if both API requests were successful
        if products_response.status_code == 200 and categories_response.status_code == 200:
            products_data = products_response.json()  # Parse JSON data for products
            categories_data = categories_response.json()  # Parse JSON data for categories

            # Render the template and pass the data
            return render_template('products.html', products=products_data, categories=categories_data)
        else:
            # Handle API errors
            return jsonify({
                "error": "Failed to fetch data from one or more APIs",
                "products_status": products_response.status_code,
                "categories_status": categories_response.status_code
            }), 500
    except Exception as e:
        # Handle any unexpected errors
        return jsonify({"error": str(e)}), 500
    
@app.route('/api/', methods=['GET'])
@login_required
def inventory():
    try:
        # URLs for the external APIs
        products_api = "http://127.0.0.1:5000/api/products"
        categories_api = "http://127.0.0.1:5000/api/product_categories"

        # Fetch data from the external APIs
        products_response = requests.get(products_api)
        categories_response = requests.get(categories_api)

        # Check if the API calls were successful
        if products_response.status_code == 200 and categories_response.status_code == 200:
            products = products_response.json()
            categories = categories_response.json()

            # Pass the data to the template
            return render_template('inventory.html', products=products, categories=categories)
        else:
            # Handle API errors
            return jsonify({"message": "Failed to fetch data from APIs!"}), 500

    except requests.exceptions.RequestException as e:
        # Handle connection errors or other issues
        return jsonify({"message": f"Error fetching data: {str(e)}"}), 500

@app.route('/api/reports',)
@login_required
def reports():
    return render_template('reports.html')

# Logout route
@app.route('/api/logout')
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logged out successfully!"}), 200

# Example of an API route that requires login
@app.route('/api/orders')
@login_required
def get_data():
    data = {"message": "This is secured data"}
    return jsonify(data)

### CRUD for Each Table ###

# 1. Users Table
@app.route('/api/users', methods=['GET', 'POST'])
@app.route('/api/users/<string:username>', methods=['GET', 'PUT','DELETE'])
@cross_origin()
@login_required
def manage_users(username=None):
    connection = create_connection()
    if not connection:
        return error_response("Database connection failed.")
    try:
        cursor = connection.cursor(dictionary=True)
        if request.method == 'GET':
            if username:
                # Fetch a specific user by username
                query = "SELECT * FROM Users WHERE username = %s;"
                cursor.execute(query, (username,))
                user = cursor.fetchone()
                if not user:
                    return error_response("User not found.", 404)
                return jsonify(user)
            else:
                # Fetch all users if no username is provided
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
            if not username:
                return error_response("Username is required for updating.")
            data = request.get_json()
            query = """
            UPDATE Users
            SET username = %s, password_hash = %s, role = %s, email = %s, first_name = %s, last_name = %s
            WHERE username = %s;
            """
            cursor.execute(query, (
                data['username'], data['password_hash'], data['role'], 
                data['email'], data.get('first_name'), data.get('last_name'), username
            ))
            connection.commit()
            if cursor.rowcount == 0:
                return error_response("User not found.", 404)
            return jsonify({'message': 'User updated successfully.'})
        elif request.method == 'DELETE':
            if not username:
                return error_response("Username is required for deletion.")
            query = "DELETE FROM Users WHERE username = %s;"
            cursor.execute(query, (username,))
            connection.commit()
            if cursor.rowcount == 0:
                return error_response("User not found.", 404)
            return jsonify({'message': 'User deleted successfully.'})
    except Exception as e:
        return error_response(f"An error occurred: {str(e)}")
    finally:
        connection.close()

@app.route('/api/product_categories', methods=['GET', 'POST'])
@app.route('/api/product_categories/<int:category_id>', methods=['GET', 'PUT','DELETE'])
@cross_origin()
@login_required
def manage_category(category_id=None):
    connection = create_connection()
    if not connection:
        return error_response("Database connection failed.")
    try:
        cursor = connection.cursor(dictionary=True)
        if request.method == 'GET':
            if category_id:
                # Fetch a specific category by category_id
                query = "SELECT * FROM Product_Categories WHERE category_id = %s;"
                cursor.execute(query, (category_id,))
                category = cursor.fetchone()
                if not category:
                    return error_response("Category not found.", 404)
                return jsonify(category)
            else:
                # Fetch all categories if no category_id is provided
                cursor.execute("SELECT * FROM Product_Categories;")
                return jsonify(cursor.fetchall())

        elif request.method == 'POST':
            # Create a new category
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
            if not category_id:
                return error_response("Category ID is required for updating.")
            data = request.get_json()
            # Update category details by category_id
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
            if not category_id:
                return error_response("Category ID is required for deletion.")
            # Delete category by category_id
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


@app.route('/api/products', methods=['GET', 'POST'])
@app.route('/api/products/<int:product_id>', methods=['GET', 'PUT', 'DELETE'])
@cross_origin()
@login_required
def manage_products(product_id=None):
    connection = create_connection()
    if not connection:
        return error_response("Database connection failed.")
    try:
        cursor = connection.cursor(dictionary=True)
        if request.method == 'GET':
            if product_id:
                # Fetch a specific product by product_id
                query = "SELECT * FROM Products WHERE product_id = %s;"
                cursor.execute(query, (product_id,))
                product = cursor.fetchone()
                if not product:
                    return error_response("Product not found.", 404)
                return jsonify(product)
            else:
                # Fetch all products if no product_id is provided
                cursor.execute("SELECT * FROM Products;")
                return jsonify(cursor.fetchall())

        elif request.method == 'POST':
            # Create a new product
            data = request.get_json()
            required_fields = ['product_name', 'unit_price', 'category_id', 'reorder_level']
            if not validate_data(data, required_fields):
                return error_response("Missing required fields.")
            query = """
            INSERT INTO Products (product_name, description, quantity_in_stock, unit_price, category_id, reorder_level)
            VALUES (%s, %s, %s, %s, %s, %s);
            """
            cursor.execute(query, (
                data['product_name'], data.get('description'), data.get('quantity_in_stock', 0),
                data['unit_price'], data['category_id'], data['reorder_level']
            ))
            connection.commit()
            return jsonify({'message': 'Product created successfully.', 'product_id': cursor.lastrowid}), 201

        elif request.method == 'PUT':
            if not product_id:
                return error_response("Product ID is required for updating.")
            data = request.get_json()
            # Update product details by product_id
            query = """
            UPDATE Products
            SET product_name = %s, description = %s, quantity_in_stock = %s, unit_price = %s, category_id = %s, reorder_level = %s
            WHERE product_id = %s;
            """
            cursor.execute(query, (
                data['product_name'], data.get('description'), data.get('quantity_in_stock'),
                data['unit_price'], data['category_id'], data['reorder_level'], product_id
            ))
            connection.commit()
            if cursor.rowcount == 0:
                return error_response("Product not found.", 404)
            return jsonify({'message': 'Product updated successfully.'})

        elif request.method == 'DELETE':
            if not product_id:
                return error_response("Product ID is required for deletion.")
            # Delete product by product_id
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


@app.route('/api/orders', methods=['GET', 'POST'])
@app.route('/api/orders/<int:order_id>', methods=['GET', 'PUT', 'DELETE'])
@cross_origin()
@login_required
def manage_orders(order_id=None):
    connection = create_connection()
    if not connection:
        return error_response("Database connection failed.")
    try:
        cursor = connection.cursor(dictionary=True)
        if request.method == 'GET':
            if order_id:
                # Fetch a specific order by order_id
                query = "SELECT * FROM Orders WHERE order_id = %s;"
                cursor.execute(query, (order_id,))
                order = cursor.fetchone()
                if not order:
                    return error_response("Order not found.", 404)
                return jsonify(order)
            else:
                # Fetch all orders if no order_id is provided
                cursor.execute("SELECT * FROM Orders;")
                return jsonify(cursor.fetchall())

        elif request.method == 'POST':
            # Create a new order
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
            if not order_id:
                return error_response("Order ID is required for updating.")
            data = request.get_json()
            # Update order details by order_id
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
            if not order_id:
                return error_response("Order ID is required for deletion.")
            # Delete order by order_id
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

@app.route('/api/order_items', methods=['GET', 'POST'])
@app.route('/api/order_items/<int:order_item_id>', methods=['GET', 'PUT', 'DELETE'])
@cross_origin()
@login_required
def manage_order_items(order_item_id=None):
    connection = create_connection()
    if not connection:
        return error_response("Database connection failed.")
    try:
        cursor = connection.cursor(dictionary=True)
        if request.method == 'GET':
            if order_item_id:
                # Fetch a specific order item by order_item_id
                query = "SELECT * FROM Order_Items WHERE order_item_id = %s;"
                cursor.execute(query, (order_item_id,))
                order_item = cursor.fetchone()
                if not order_item:
                    return error_response("Order item not found.", 404)
                return jsonify(order_item)
            else:
                # Fetch all order items if no order_item_id is provided
                cursor.execute("SELECT * FROM Order_Items;")
                return jsonify(cursor.fetchall())

        elif request.method == 'POST':
            # Create a new order item
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
            if not order_item_id:
                return error_response("Order item ID is required for updating.")
            data = request.get_json()
            # Update order item details by order_item_id
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
            if not order_item_id:
                return error_response("Order item ID is required for deletion.")
            # Delete order item by order_item_id
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


@app.route('/api/reports', methods=['GET', 'POST'])
@app.route('/api/reports/<int:report_id>', methods=['GET', 'PUT', 'DELETE'])
@cross_origin()
@login_required
def manage_reports(report_id=None):
    connection = create_connection()
    if not connection:
        return error_response("Database connection failed.")
    try:
        cursor = connection.cursor(dictionary=True)
        if request.method == 'GET':
            if report_id:
                # Fetch a specific report by report_id
                query = "SELECT * FROM Reports WHERE report_id = %s;"
                cursor.execute(query, (report_id,))
                report = cursor.fetchone()
                if not report:
                    return error_response("Report not found.", 404)
                return jsonify(report)
            else:
                # Fetch all reports if no report_id is provided
                cursor.execute("SELECT * FROM Reports;")
                return jsonify(cursor.fetchall())

        elif request.method == 'POST':
            # Create a new report
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
            if not report_id:
                return error_response("Report ID is required for updating.")
            data = request.get_json()
            # Update report details by report_id
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
            if not report_id:
                return error_response("Report ID is required for deletion.")
            # Delete report by report_id
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


@app.route('/api/invoices', methods=['GET', 'POST'])
@app.route('/api/invoices/<int:invoice_id>', methods=['GET', 'PUT', 'DELETE'])
@cross_origin()
@login_required
def manage_invoices(invoice_id=None):
    connection = create_connection()
    if not connection:
        return error_response("Database connection failed.")
    try:
        cursor = connection.cursor(dictionary=True)
        if request.method == 'GET':
            if invoice_id:
                # Fetch a specific invoice by invoice_id
                query = "SELECT * FROM Invoices WHERE invoice_id = %s;"
                cursor.execute(query, (invoice_id,))
                invoice = cursor.fetchone()
                if not invoice:
                    return error_response("Invoice not found.", 404)
                return jsonify(invoice)
            else:
                # Fetch all invoices if no invoice_id is provided
                cursor.execute("SELECT * FROM Invoices;")
                return jsonify(cursor.fetchall())

        elif request.method == 'POST':
            # Create a new invoice
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
            if not invoice_id:
                return error_response("Invoice ID is required for updating.")
            data = request.get_json()
            # Update invoice details by invoice_id
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
            if not invoice_id:
                return error_response("Invoice ID is required for deletion.")
            # Delete invoice by invoice_id
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