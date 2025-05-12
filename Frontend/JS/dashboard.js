document.addEventListener('DOMContentLoaded', () => {
    const fetchAndPopulateDashboard = async () => {
        try {
            // Fetch products and orders data
            const [productsResponse, ordersResponse] = await Promise.all([
                fetch('http://127.0.0.1:5000/api/products', {
					method: 'GET',
				    credentials: 'include',}),
                fetch('http://127.0.0.1:5000/api/orders', {
					method: 'GET',
				    credentials: 'include',})
            ]);

            // Check if both API responses are OK
            if (!productsResponse.ok) {
                throw new Error(`Failed to fetch products: Status ${productsResponse.status}`);
            }
            if (!ordersResponse.ok) {
                throw new Error(`Failed to fetch orders: Status ${ordersResponse.status}`);
            }

            const products = await productsResponse.json();
            const orders = await ordersResponse.json();
			
			// Log raw response to debug
			console.log('Products:', products);
			console.log('Orders:', orders);
			
			// Check if they are arrays
			if (!Array.isArray(products)) {
			    throw new Error('Products response is not an array');
			}
			if (!Array.isArray(orders)) {
			    throw new Error('Orders response is not an array');
			}
			
			const rawProducts = await productsResponse.text();
			const rawOrders = await ordersResponse.text();
			console.log('Raw Products Response:', rawProducts);
			console.log('Raw Orders Response:', rawOrders);
			
			// Inside fetchAndPopulateDashboard
			const totalInventoryElem = document.getElementById('total-inventory-value');
			if (totalInventoryElem) {
			    totalInventoryElem.textContent = `$${totalInventoryValue}`;
			} else {
			    console.error('Element #total-inventory-value not found in DOM.');
			}

			const stockOnHandElem = document.getElementById('stock-on-hand');
			if (stockOnHandElem) {
			    stockOnHandElem.textContent = `${stockOnHand} items`;
			} else {
			    console.error('Element #stock-on-hand not found in DOM.');
			}

			const lowStockElem = document.getElementById('low-stock');
			if (lowStockElem) {
			    lowStockElem.textContent = `${lowStock} items`;
			} else {
			    console.error('Element #low-stock not found in DOM.');
			}

			const outOfStockElem = document.getElementById('out-of-stock');
			if (outOfStockElem) {
			    outOfStockElem.textContent = `${outOfStock} items`;
			} else {
			    console.error('Element #out-of-stock not found in DOM.');
			}

			const pendingOrdersElem = document.getElementById('pending-orders');
			if (pendingOrdersElem) {
			    pendingOrdersElem.textContent = `${pendingOrders} orders`;
			} else {
			    console.error('Element #pending-orders not found in DOM.');
			}
			
            // Total inventory value
            const totalInventoryValue = products.reduce((total, product) => total + (product.unit_price * product.quantity_in_stock), 0).toFixed(2);

            // Stock on hand (total quantity in stock)
            const stockOnHand = products.reduce((total, product) => total + product.quantity_in_stock, 0);

            // Low stock (products with stock less than 50% of reorder level)
            const lowStock = products.filter(product => product.quantity_in_stock <= product.reorder_level * 0.5).length;

            // Out of stock (products with zero quantity in stock)
            const outOfStock = products.filter(product => product.quantity_in_stock === 0).length;

            // Pending orders (orders with status 'Pending')
            const pendingOrders = orders.filter(order => order.status === 'Pending').length;

            // Update HTML content with fetched values
            document.getElementById('total-inventory-value').textContent = `$${totalInventoryValue}`;
            document.getElementById('stock-on-hand').textContent = `${stockOnHand} items`;
            document.getElementById('low-stock').textContent = `${lowStock} items`;
            document.getElementById('out-of-stock').textContent = `${outOfStock} items`;
            document.getElementById('pending-orders').textContent = `${pendingOrders} orders`;

            // Sort the orders by order_date (most recent first)
            orders.sort((a, b) => new Date(b.order_date) - new Date(a.order_date));

            // Get the first 10 orders (most recent)
            const recentOrders = orders.slice(0, 10);

            recentOrders.forEach(order => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${order.order_id}</td>
                    <td>${new Date(order.order_date).toLocaleDateString()}</td>
                    <td>${order.total_amount}</td>
                    <td>${order.status}</td>
                `;
            });

        } catch (error) {
            console.error('Error fetching data for dashboard:', error);
            // Display error message in the dashboard
            document.getElementById('dashboard-error-message').textContent = 'Failed to load dashboard data. Please try again later.';
        }
    };

    const fetchAndPopulateOrders = async () => {
        try {
            // Fetch the orders
            const ordersResponse = await fetch('http://127.0.0.1:5000/api/orders',{
				method: 'GET',
				credentials: 'include',}); // Adjust the API endpoint
            if (!ordersResponse.ok) {
                throw new Error(`HTTP error! Status: ${ordersResponse.status}`);
            }
            const orders = await ordersResponse.json();

            // Sort the orders by date (most recent first)
            orders.sort((a, b) => new Date(b.order_date) - new Date(a.order_date));

            // Get the first 10 orders
            const recentOrders = orders.slice(0, 10);

            // Populate the dashboard with order data
            const tableBody = document.querySelector('#orders-table-body'); // Adjust to the correct selector
            tableBody.innerHTML = ''; // Clear any existing rows

            recentOrders.forEach((order) => {
                const row = document.createElement('tr');

                row.innerHTML = `
                    <td>${order.order_id}</td>
                    <td>${new Date(order.order_date).toLocaleDateString()}</td>
                    <td>${order.total_amount}</td>
                    <td>${order.status}</td>
                `;

                tableBody.appendChild(row);
            });
        } catch (error) {
            console.error('Error fetching orders:', error);

            const tableBody = document.querySelector('#orders-table-body');
            tableBody.innerHTML = `
                <tr>
                    <td colspan="4" style="text-align: center; color: red;">
                        Failed to load orders. Please try again later.
                    </td>
                </tr>
            `;
        }
    };

    // Call the functions to fetch and populate the dashboard
    fetchAndPopulateDashboard();
    fetchAndPopulateOrders();
});
