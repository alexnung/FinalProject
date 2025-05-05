document.addEventListener('DOMContentLoaded', () => {
    const fetchAndPopulateInventory = () => {
        Promise.all([
            fetch('http://127.0.0.1:5000/api/products'),
            fetch('http://127.0.0.1:5000/api/product_categories')
        ])
            .then(([productsResponse, categoriesResponse]) => {
                if (!productsResponse.ok) {
                    throw new Error(`Failed to fetch products: Status ${productsResponse.status}`);
                }
                if (!categoriesResponse.ok) {
                    throw new Error(`Failed to fetch categories: Status ${categoriesResponse.status}`);
                }
                return Promise.all([productsResponse.json(), categoriesResponse.json()]);
            })
            .then(([products, categories]) => {
                console.log('Products:', products);
                console.log('Categories:', categories);

                // Map categories
                const categoryMap = {};
                categories.forEach((category) => {
                    categoryMap[category.category_id] = category.category_name;
                });

                // Populate inventory table
                const tableBody = document.getElementById('inventory-table-body');
                tableBody.innerHTML = ''; // Clear existing rows

                // Collect inventory alerts
                const alerts = [];

                products.forEach((product) => {
                    const row = document.createElement('tr');
                    const categoryName = categoryMap[product.category_id] || 'Unknown';

                    // Check for inventory alerts
                    if (product.quantity_in_stock <= product.reorder_level * 1.5 || product.quantity_in_stock === 0) {
                        const alertType =
                            product.quantity_in_stock === 0
                                ? 'Out of Stock'
                                : 'Low Stock';
                        alerts.push(
                            `${product.product_name} (${categoryName}): ${alertType} (Stock: ${product.quantity_in_stock}, Reorder Level: ${product.reorder_level})`
                        );
                    }

                    row.innerHTML = `
                        <td>${product.product_id}</td>
                        <td>${product.product_name}</td>
                        <td>${categoryName}</td>
                        <td>${product.quantity_in_stock}</td>
                        <td>${product.reorder_level}</td>
                    `;

                    tableBody.appendChild(row);
                });

                // Debugging alerts
                console.log('Generated Alerts:', alerts);

                // Populate alerts section
                const alertsList = document.getElementById('inventory-alerts-list');
                alertsList.innerHTML = ''; // Clear existing alerts

                if (alerts.length === 0) {
                    alertsList.innerHTML = '<li>No inventory alerts at this time.</li>';
                } else {
                    alerts.forEach((alert) => {
                        const alertItem = document.createElement('li');
                        alertItem.textContent = alert;
                        alertsList.appendChild(alertItem);
                    });
                }
            })
            .catch((error) => {
                console.error('Error fetching inventory data:', error);

                // Clear the table and show an error message
                const tableBody = document.getElementById('inventory-table-body');
                if (tableBody) {
                    tableBody.innerHTML = `
                        <tr>
                            <td colspan="5" style="text-align: center; color: red;">
                                Failed to load inventory data. Please try again later.
                            </td>
                        </tr>
                    `;
                }

                // Clear the alerts section and show an error message
                const alertsList = document.getElementById('inventory-alerts-list');
                if (alertsList) {
                    alertsList.innerHTML = `
                        <li style="color: red;">Failed to load inventory alerts. Please try again later.</li>
                    `;
                }
            });
    };

    // Trigger the API fetch and table update
    fetchAndPopulateInventory();
});
