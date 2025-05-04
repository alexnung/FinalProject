document.addEventListener('DOMContentLoaded', () => {
    const fetchAndPopulateOrders = () => {
        fetch('http://127.0.0.1:5000/api/orders')
            .then((response) => {
                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }
                return response.json();
            })
            .then((orders) => {
                console.log('API Response:', orders); // Log response for debugging
                
                const tableBody = document.getElementById('orders-table-body');
                tableBody.innerHTML = ''; // Clear existing rows

                orders.forEach((order) => {
                    const row = document.createElement('tr');

                    // Safely parse `total_amount` and ensure it is a number
                    const totalAmount = isNaN(order.total_amount)
                        ? 0
                        : parseFloat(order.total_amount);

                    row.innerHTML = `
                        <td>${order.order_id}</td>
                        <td>${new Date(order.order_date).toLocaleDateString()}</td>
						<td>${order.customer_id}</td>
                        <td>${order.status}</td>
                        <td>${totalAmount.toFixed(2)}</td>
                        <td>${order.payment_status}</td>
                        <td>${order.shipping_address}</td>
                    `;

                    tableBody.appendChild(row);
                });
            })
            .catch((error) => {
                console.error('Error fetching orders:', error);
                const tableBody = document.getElementById('orders-table-body');
                tableBody.innerHTML = `
                    <tr>
                        <td colspan="6" style="text-align: center; color: red;">
                            Failed to load orders. Please try again later.
                        </td>
                    </tr>
                `;
            });
    };

    // Trigger the API fetch and table update
    fetchAndPopulateOrders();
});
