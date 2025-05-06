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


		
		document.addEventListener('DOMContentLoaded', () => {
		    const apiUrl = 'http://127.0.0.1:5000/api/orders'; // Adjust your API URL as needed
		    const orderForm = document.getElementById('orderForm');
		    const orderFormElement = document.getElementById('orderFormElement');
		    const orderIdSelect = document.getElementById('orderId');
		    const orderItemsContainer = document.getElementById('orderItemsContainer');
		    const createOrderBtn = document.getElementById('createOrderBtn');
		    const updateOrderBtn = document.getElementById('updateOrderBtn');

		    // Fetch and populate the order ID select options
		    const fetchOrderIds = async () => {
		        try {
		            const ordersResponse = await fetch(apiUrl);
		            const orders = await ordersResponse.json();
		            orderIdSelect.innerHTML = ''; // Clear the current options

		            orders.forEach(order => {
		                const option = document.createElement('option');
		                option.value = order.order_id;
		                option.textContent = `Order #${order.order_id}`;
		                orderIdSelect.appendChild(option);
		            });
		        } catch (error) {
		            console.error('Error fetching order IDs:', error);
		        }
		    };

		    // Fetch and populate the order items (for update)
		    const fetchOrderItems = async (orderId) => {
		        try {
		            const response = await fetch(`${apiUrl}/${orderId}/items`);
		            const orderItems = await response.json();
		            orderItemsContainer.innerHTML = ''; // Clear the current items

		            orderItems.forEach(item => {
		                const itemDiv = document.createElement('div');
		                itemDiv.classList.add('order-item');
		                itemDiv.innerHTML = `
		                    <label>Product ID:</label>
		                    <input type="number" class="product-id" value="${item.product_id}" required>
		                    <label>Quantity:</label>
		                    <input type="number" class="quantity" value="${item.quantity}" required>
		                    <label>Unit Price:</label>
		                    <input type="number" class="unit-price" value="${item.unit_price}" required>
		                    <button class="delete-item-btn">Delete</button>
		                `;
		                orderItemsContainer.appendChild(itemDiv);

		                // Add event listener to delete the item
		                itemDiv.querySelector('.delete-item-btn').addEventListener('click', () => {
		                    itemDiv.remove(); // Remove the item from the form
		                });
		            });
		        } catch (error) {
		            console.error('Error fetching order items:', error);
		        }
		    };

		    // Handle Create Order
		    createOrderBtn.addEventListener('click', () => {
		        orderForm.style.display = 'block';
		        orderFormElement.reset();
		        document.getElementById('formTitle').textContent = 'Create Order';
		        orderIdSelect.style.display = 'none'; // Hide Order ID select (not needed for create)
		    });

		    // Handle Update Order
		    updateOrderBtn.addEventListener('click', () => {
		        orderForm.style.display = 'block';
		        orderFormElement.reset();
		        document.getElementById('formTitle').textContent = 'Update Order';
		        orderIdSelect.style.display = 'inline'; // Show Order ID select for updating
		    });

		    // Handle Form Submission
		    orderFormElement.addEventListener('submit', async (event) => {
		        event.preventDefault();

		        const formData = new FormData(orderFormElement);
		        const orderId = formData.get('orderId');
		        const customerId = formData.get('customerId');
		        const status = formData.get('status');
		        const paymentStatus = formData.get('paymentStatus');
		        const shippingAddress = formData.get('shippingAddress');

		        // Get order items from the form
		        const orderItems = Array.from(orderItemsContainer.querySelectorAll('.order-item')).map(itemDiv => {
		            const productId = itemDiv.querySelector('.product-id').value;
		            const quantity = itemDiv.querySelector('.quantity').value;
		            const unitPrice = itemDiv.querySelector('.unit-price').value;
		            return { product_id: productId, quantity, unit_price: unitPrice };
		        });

		        const orderData = {
		            customer_id: customerId,
		            status,
		            payment_status: paymentStatus,
		            shipping_address: shippingAddress,
		            order_items: orderItems
		        };

		        try {
		            let response;
		            if (orderId) {
		                // Update existing order
		                response = await fetch(`${apiUrl}/${orderId}`, {
		                    method: 'PUT',
		                    body: JSON.stringify(orderData),
		                    headers: { 'Content-Type': 'application/json' }
		                });
		            } else {
		                // Create new order
		                response = await fetch(apiUrl, {
		                    method: 'POST',
		                    body: JSON.stringify(orderData),
		                    headers: { 'Content-Type': 'application/json' }
		                });
		            }

		            if (!response.ok) {
		                throw new Error('Failed to save order');
		            }

		            alert('Order saved successfully!');
		            orderForm.style.display = 'none'; // Close the form
		            fetchOrderIds(); // Refresh the order IDs for the next update
		        } catch (error) {
		            console.error('Error saving order:', error);
		            alert('Error saving order.');
		        }
		    });

		  // Initialize by fetching order IDs and populating them
		fetchOrderIds();  
		});
		

