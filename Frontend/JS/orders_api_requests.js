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

	document.addEventListener('DOMContentLoaded', () => {
		    const apiUrlOrders = 'http://127.0.0.1:5000/api/orders';
		    const apiUrlProducts = 'http://127.0.0.1:5000/api/products';

		    const updateOrderBtn = document.getElementById('updateOrderBtn');
		    const updateOrderModal = document.getElementById('updateOrderModal');
		    const cancelUpdateBtn = document.getElementById('cancelUpdateBtn');
		    const orderIdSelect = document.getElementById('update_order_id');
		    const productSelect = document.getElementById('update_product_id');
		    const addProductBtn = document.getElementById('addProductBtn');
		    const orderProductsTable = document.getElementById('orderProductsTable').getElementsByTagName('tbody')[0];
		    const totalAmountInput = document.getElementById('update_total_amount');
		    const updateOrderForm = document.getElementById('updateOrderForm');

		    let selectedProducts = []; // Array to store products added to the order
		    let products = []; // Store the fetched products

		    // Open the update order modal
		    updateOrderBtn.addEventListener('click', () => {
		        updateOrderModal.style.display = 'flex';
		        fetchOrders(); // Fetch and populate orders
		        fetchProducts(); // Fetch and populate products
		    });

		    // Close the update order modal
		    cancelUpdateBtn.addEventListener('click', () => {
		        updateOrderModal.style.display = 'none';
		    });

		    // Fetch and populate orders dropdown
		    const fetchOrders = async () => {
		        try {
		            orderIdSelect.innerHTML = '<option value="">Select an Order</option>'; // Clear dropdown
		            const response = await fetch(apiUrlOrders);
		            const orders = await response.json();
		            console.log('Orders fetched:', orders); // Debugging line
		            orders.forEach(order => {
		                const option = document.createElement('option');
		                option.value = order.order_id;
		                option.textContent = `Order #${order.order_id}`;
		                orderIdSelect.appendChild(option);
		            });
		        } catch (error) {
		            console.error('Error fetching orders:', error);
		        }
		    };

		    // Fetch and populate products dropdown
		    const fetchProducts = async () => {
		        try {
		            const response = await fetch(apiUrlProducts);
		            const productData = await response.json();
		            console.log('Products fetched:', productData); // Debugging line
		            products = productData; // Store products in the products array
		            populateProductSelect(); // Populate the product dropdown after fetching
		        } catch (error) {
		            console.error('Error fetching products:', error);
		        }
		    };

		    // Populate the product select dropdown
		    const populateProductSelect = () => {
		        if (!productSelect) {
		            console.error("product_id element is missing in the HTML.");
		            return;
		        }

		        // Debugging the state of the products array
		        console.log('Products array:', products);

		        // Clear existing options in the product dropdown
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

		        // Debugging if the dropdown is populated
		        console.log('Dropdown populated with products');
		    };

		    // Add product to the order
		    addProductBtn.addEventListener('click', () => {
		        const productId = document.getElementById('update_product_id').value;
		        const quantity = document.getElementById('update_quantity').value;

		        if (!productId || !quantity) {
		            alert('Please select a product and quantity.');
		            return;
		        }

		        const selectedProduct = {
		            product_id: productId,
		            quantity: quantity
		        };

		        selectedProducts.push(selectedProduct);
		        updateOrderProductList();
		        updateTotalAmount();
		    });

		    // Update the list of products in the order
		    const updateOrderProductList = () => {
		        orderProductsTable.innerHTML = '';
		        selectedProducts.forEach(product => {
		            const row = document.createElement('tr');
		            row.innerHTML = `
		                <td>${product.product_id}</td>
		                <td>${product.quantity}</td>
		                <td><button class="removeProductBtn">Remove</button></td>
		            `;
		            orderProductsTable.appendChild(row);

		            row.querySelector('.removeProductBtn').addEventListener('click', () => {
		                selectedProducts = selectedProducts.filter(p => p !== product);
		                updateOrderProductList();
		                updateTotalAmount();
		            });
		        });
		    };

		    // Calculate the total amount based on selected products and quantities
		    const updateTotalAmount = async () => {
		        let totalAmount = 0;

		        for (const product of selectedProducts) {
		            const productDetails = await fetchProductDetails(product.product_id);
		            totalAmount += productDetails.unit_price * product.quantity;
		        }

		        totalAmountInput.value = totalAmount.toFixed(2);
		    };

		    // Fetch product details (e.g., price) for calculating total amount
		    const fetchProductDetails = async (productId) => {
		        try {
		            const response = await fetch(`${apiUrlProducts}/${productId}`);
		            const product = await response.json();
		            return product;
		        } catch (error) {
		            console.error('Error fetching product details:', error);
		            return { unit_price: 0 };
		        }
		    };

		    // Submit the update order form
		    updateOrderForm.addEventListener('submit', async (e) => {
		        e.preventDefault();

		        const orderId = orderIdSelect.value;
		        const customerId = document.getElementById('customer_id').value;

		        if (!orderId) {
		            alert('Please select an order to update.');
		            return;
		        }

				const orderData = {
				    customer_id: document.getElementById("update_customer_id").value.trim(), // Customer ID from input
				    status: document.getElementById("update_status").value, // Status from the dropdown
				    total_amount: parseFloat(document.getElementById("update_total_amount").value.trim()), // Total amount from input, parsed to a float
				    payment_status: document.getElementById("update_payment_status").value, // Payment status from the dropdown
				    shipping_address: document.getElementById("update_shipping_address")?.value.trim() || null, // Optional shipping address, default to null if not present
				};




		        try {
		            const response = await fetch(`${apiUrlOrders}/${orderId}`, {
		                method: 'PUT',
		                headers: {
		                    'Content-Type': 'application/json'
		                },
		                body: JSON.stringify(orderData)
		            });

		            if (response.ok) {
		                alert('Order updated successfully!');
		                updateOrderModal.style.display = 'none';
		            } else {
		                alert('Failed to update order.');
		            }
		        } catch (error) {
		            console.error('Error updating order:', error);
		            alert('Error updating order.');
		        }
		    });
		});
