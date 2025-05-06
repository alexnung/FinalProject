document.addEventListener('DOMContentLoaded', () => {
    const apiUrl = 'http://127.0.0.1:5000/api/orders'; // Adjust your API URL as needed

    // Fetch and populate orders table
    const fetchAndPopulateOrders = async () => {
        try {
            const ordersResponse = await fetch(apiUrl);
            const orders = await ordersResponse.json();
            const tableBody = document.querySelector('#orders-table-body');
            tableBody.innerHTML = ''; // Clear existing rows

            orders.forEach((order) => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${order.order_id}</td>
                    <td>${new Date(order.order_date).toLocaleDateString()}</td>
                    <td>${order.customer_id}</td>
                    <td>${order.status}</td>
                    <td>$${order.total_amount}</td>
                    <td>${order.payment_status}</td>
                    <td>${order.shipping_address}</td>
                    <td>
                        <button class="delete-order-btn" data-order-id="${order.order_id}">Delete</button>
                    </td>
                `;
                tableBody.appendChild(row);
            });

            // Add event listeners to delete buttons
            document.querySelectorAll('.delete-order-btn').forEach((button) => {
                button.addEventListener('click', async (e) => {
                    const orderId = e.target.dataset.orderId;
                    if (confirm(`Are you sure you want to delete order #${orderId}?`)) {
                        await deleteOrder(orderId);
                    }
                });
            });
        } catch (error) {
            console.error('Error fetching orders:', error);
            alert('Error loading orders.');
        }
    };

    // Function to delete an order
    const deleteOrder = async (orderId) => {
        try {
            const response = await fetch(`${apiUrl}?order_id=${orderId}`, {
                method: 'DELETE',
            });

            if (!response.ok) {
                throw new Error(`Failed to delete order: ${response.status}`);
            }

            alert('Order deleted successfully!');
            fetchAndPopulateOrders(); // Refresh the orders table
        } catch (error) {
            console.error('Error deleting order:', error);
            alert('Error deleting order.');
        }
    };
	
    // Initialize orders table on page load
    fetchAndPopulateOrders();
});

let products = []; // Store available products fetched from backend
let orders = []; // Store existing orders for updating
let orderItems = []; // Temporary store for items in the order

// Fetch available products from the database when creating/updating an order
function fetchProducts() {
    fetch('http://127.0.0.1:5000/api/products')  // Your backend API for fetching products
        .then(response => response.json())
        .then(data => {
            products = data;
            populateProductSelect();
        })
        .catch(error => console.error("Error fetching products:", error));
}

// Fetch existing orders when updating an order
function fetchOrders() {
    fetch('http://127.0.0.1:5000/api/orders')  // Your backend API for fetching orders
        .then(response => response.json())
        .then(data => {
            orders = data;
            populateOrderSelect();
        })
        .catch(error => console.error("Error fetching orders:", error));
}

// Populate product select options dynamically
function populateProductSelect() {
    const productSelect = document.getElementById("product_id");
    const updateProductSelect = document.getElementById("update_product_id");

    // Clear previous options
    productSelect.innerHTML = "";
    updateProductSelect.innerHTML = "";

    // Add default option to the select dropdowns
    const defaultOption = document.createElement("option");
    defaultOption.value = "";
    defaultOption.textContent = "Select a product";
    productSelect.appendChild(defaultOption);
    updateProductSelect.appendChild(defaultOption.cloneNode(true));

    // Add product options dynamically
    products.forEach(product => {
        const option = document.createElement("option");
        option.value = product.product_id;
        option.textContent = `${product.product_name} - $${product.unit_price}`;
        productSelect.appendChild(option);
        updateProductSelect.appendChild(option.cloneNode(true));
    });
}

// Populate existing order select options dynamically (for update)
function populateOrderSelect() {
    const orderSelect = document.getElementById("existing_order_id");

    // Clear previous options
    orderSelect.innerHTML = "";

    // Add default option
    const defaultOption = document.createElement("option");
    defaultOption.value = "";
    defaultOption.textContent = "Select an order";
    orderSelect.appendChild(defaultOption);

    // Add order options dynamically
    orders.forEach(order => {
        const option = document.createElement("option");
        option.value = order.order_id;
        option.textContent = `Order ID: ${order.order_id} - ${order.status}`;
        orderSelect.appendChild(option);
    });
}

// Show the Create Order Form and populate the product dropdown
document.getElementById("createOrderBtn").addEventListener("click", function() {
    fetchProducts();  // Fetch products for creating an order
    toggleForm('create-order-form');  // Show the form
});

// Show the Update Order Form and populate the existing orders and product dropdown
document.getElementById("updateOrderBtn").addEventListener("click", function() {
    fetchOrders();  // Fetch existing orders for updating
    fetchProducts();  // Fetch products for updating an order
    toggleForm('update-order-form');  // Show the form
});

// Add item to the order in the Create Order form
function addItem() {
    const productId = parseInt(document.getElementById("product_id").value);
    const quantity = parseInt(document.getElementById("quantity").value);
    const product = products.find(p => p.product_id === productId);
    
    if (product && quantity > 0) {
        const subtotal = product.unit_price * quantity;
        orderItems.push({ product, quantity, subtotal });
        updateOrderItemsList();
        updateTotalAmount();
    } else {
        alert("Invalid product or quantity.");
    }
}

// Add or update an item in the order in the Update Order form
function updateItem() {
    const orderId = parseInt(document.getElementById("existing_order_id").value);
    const shippingAddress = document.getElementById("update_shipping_address").value;
    const status = document.getElementById("update_status").value;
    const paymentStatus = document.getElementById("update_payment_status").value;

    const productId = parseInt(document.getElementById("update_product_id").value);
    const quantity = parseInt(document.getElementById("update_quantity").value);
    
    const product = products.find(p => p.product_id === productId);
    if (product && quantity > 0) {
        const subtotal = product.unit_price * quantity;

        // Check if the item already exists in the order
        let existingItem = orderItems.find(item => item.product.product_id === productId);
        if (existingItem) {
            existingItem.quantity = quantity;
            existingItem.subtotal = subtotal;
        } else {
            orderItems.push({ product, quantity, subtotal });
        }

        updateOrderItemsList();
        updateTotalAmount();
    } else {
        alert("Invalid product or quantity.");
    }
}

// Delete an item from the order in the Update Order form
function deleteItem(productId) {
    const itemIndex = orderItems.findIndex(item => item.product.product_id === productId);
    if (itemIndex !== -1) {
        orderItems.splice(itemIndex, 1);  // Remove item from the order
        updateOrderItemsList();
        updateTotalAmount();
    }
}

// Update the list of items in the order (both for Create and Update Order)
function updateOrderItemsList() {
    const orderItemsList = document.getElementById("orderItemsList");
    const updateOrderItemsList = document.getElementById("updateOrderItemsList");

    // Clear the current list
    orderItemsList.innerHTML = "";
    updateOrderItemsList.innerHTML = "";

    // Add the items to the lists dynamically
    orderItems.forEach(item => {
        const li = document.createElement("li");
        li.textContent = `${item.product.product_name} x${item.quantity} - $${item.subtotal.toFixed(2)}`;

        // Add a delete button for update orders
        const deleteButton = document.createElement("button");
        deleteButton.textContent = "Delete";
        deleteButton.onclick = () => deleteItem(item.product.product_id);  // Delete functionality
        li.appendChild(deleteButton);

        orderItemsList.appendChild(li);
        updateOrderItemsList.appendChild(li.cloneNode(true));  // For the Update Order list
    });
}

// Calculate total amount for the order
function updateTotalAmount() {
    const totalAmount = orderItems.reduce((total, item) => total + item.subtotal, 0);
    document.getElementById("totalAmount").textContent = totalAmount.toFixed(2);
    document.getElementById("updateTotalAmount").textContent = totalAmount.toFixed(2);  // For Update Order
}

// Handle order creation
document.getElementById("createOrderForm").addEventListener("submit", function(e) {
    e.preventDefault();

    const customerId = document.getElementById("customer_id").value;
    const shippingAddress = document.getElementById("shipping_address").value;
    const status = document.getElementById("status").value;
    const paymentStatus = document.getElementById("payment_status").value;

    const orderData = {
        customer_id: customerId,
        shipping_address: shippingAddress,
        status: status,
        payment_status: paymentStatus,
        items: orderItems,
        total_amount: orderItems.reduce((total, item) => total + item.subtotal, 0)
    };

    fetch('/api/createOrder', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(orderData)
    })
    .then(response => response.json())
    .then(data => {
        alert("Order Created Successfully!");
        // Reset the form
        document.getElementById("createOrderForm").reset();
        orderItems = [];
        updateOrderItemsList();
        updateTotalAmount();
        toggleForm('create-order-form');  // Close form after creation
    });
});

// Handle updating an existing order
document.getElementById("updateOrderForm").addEventListener("submit", function(e) {
    e.preventDefault();

    const orderId = parseInt(document.getElementById("existing_order_id").value);
    const shippingAddress = document.getElementById("update_shipping_address").value;
    const status = document.getElementById("update_status").value;
    const paymentStatus = document.getElementById("update_payment_status").value;

    const orderData = {
        order_id: orderId,
        shipping_address: shippingAddress,
        status: status,
        payment_status: paymentStatus,
        items: orderItems,
        total_amount: orderItems.reduce((total, item) => total + item.subtotal, 0)
    };

    fetch(`/api/updateOrder/${orderId}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(orderData)
    })
    .then(response => response.json())
    .then(data => {
        alert("Order Updated Successfully!");
        // Reset the form
        orderItems = [];
        updateOrderItemsList();
        updateTotalAmount();
        toggleForm('update-order-form');  // Close form after update
    });
});

// Toggle visibility of a form
function toggleForm(formId) {
    const form = document.getElementById(formId);
    form.style.display = (form.style.display === "none" || form.style.display === "") ? "block" : "none";
}
