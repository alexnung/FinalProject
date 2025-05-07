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
            const response = await fetch(`${apiUrl}/${orderId}`, {
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
	let orderItems = []; // Temporary store for items in the order
	
	// Toggle the visibility of the Create Order form
	function toggleCreateOrderForm() {
	    const createOrderForm = document.getElementById("create-order-form");
	
	    // Check the current state of the form visibility
	    if (createOrderForm.style.display === "none" || createOrderForm.style.display === "") {
	        fetchProducts(); // Fetch products before displaying the form
	        createOrderForm.style.display = "block"; // Show the form
	    } else {
	        createOrderForm.style.display = "none"; // Hide the form
	    }
	}
	
	// Fetch available products from the database
	function fetchProducts() {
	    fetch('http://127.0.0.1:5000/api/products') // Replace with your backend API URL
	        .then(response => response.json())
	        .then(data => {
	            products = data;
	            populateProductSelect();
	        })
	        .catch(error => console.error("Error fetching products:", error));
	}
	
	// Populate product dropdown options dynamically
	function populateProductSelect() {
	    const productSelect = document.getElementById("product_id");
	
	    if (!productSelect) {
	        console.error("product_id element is missing in the HTML.");
	        return;
	    }
	
	    // Clear previous options
	    productSelect.innerHTML = "";
	
	    // Add default option
	    const defaultOption = document.createElement("option");
	    defaultOption.value = "";
	    defaultOption.textContent = "Select a product";
	    productSelect.appendChild(defaultOption);
	
	    // Add product options dynamically
	    products.forEach(product => {
	        const option = document.createElement("option");
	        option.value = product.product_id;
	        option.textContent = `${product.product_name} - $${product.unit_price}`;
	        productSelect.appendChild(option);
	    });
	}
	
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
	
	// Update the list of items in the order
	function updateOrderItemsList() {
	    const orderItemsList = document.getElementById("orderItemsList");
	
	    // Clear the current list
	    orderItemsList.innerHTML = "";
	
	    // Add the items to the list dynamically
	    orderItems.forEach(item => {
	        const li = document.createElement("li");
	        li.textContent = `${item.product.product_name} x${item.quantity} - $${item.subtotal.toFixed(2)}`;
	        orderItemsList.appendChild(li);
	    });
	}
	
	// Calculate total amount for the order
	function updateTotalAmount() {
	    const totalAmount = orderItems.reduce((total, item) => total + item.subtotal, 0);
	    document.getElementById("totalAmount").textContent = totalAmount.toFixed(2);
	}
	
	// Handle order creation
	document.getElementById("createOrderForm").addEventListener("submit", async function (e) {
	    e.preventDefault(); // Prevent the default form submission behavior

	    const customerId = document.getElementById("customer_id").value.trim();
	    const shippingAddress = document.getElementById("shipping_address").value.trim();
	    const status = document.getElementById("status").value.trim();
	    const paymentStatus = document.getElementById("payment_status").value.trim();

	    // Check for missing fields
	    if (!customerId || !shippingAddress || !status || !paymentStatus) {
	        alert("Please fill out all required fields.");
	        return;
	    }

	    // Check if there are any items in the order
	    if (orderItems.length === 0) {
	        alert("Please add at least one product to the order.");
	        return;
	    }

	    // Prepare the order data
	    const orderData = {
	        customer_id: customerId,
	        shipping_address: shippingAddress,
	        status: status,
	        payment_status: paymentStatus,
	        items: orderItems.map(item => ({
	            product_id: item.product.product_id, 
	            quantity: item.quantity,
	            subtotal: item.subtotal
	        })),
	        total_amount: orderItems.reduce((total, item) => total + item.subtotal, 0),
	    };

	    // Log the order data to debug
	    console.log("Order Data:", orderData);

	    try {
	        const response = await fetch('http://127.0.0.1:5000/api/orders', {
	            method: 'POST',
	            headers: { 'Content-Type': 'application/json' },
	            body: JSON.stringify(orderData),
	        });

	        if (!response.ok) {
	            const errorData = await response.json();
	            console.error("Error response from server:", errorData);
	            throw new Error(errorData.message || "Failed to create order.");
	        }

	        const result = await response.json();
	        alert("Order Created Successfully!");
	        console.log("Order Details:", result);

	        // Reset the form
	        document.getElementById("createOrderForm").reset();
	        orderItems = [];
	        updateOrderItemsList();
	        updateTotalAmount();
	        toggleCreateOrderForm(); // Hide the form after successful creation
	    } catch (error) {
	        console.error("Error creating order:", error);
	        alert(`Failed to create the order: ${error.message}`);
	    }
	});

