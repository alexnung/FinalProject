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

            const categoryMap = {};
            categories.forEach((category) => {
                categoryMap[category.category_id] = category.category_name;
            });

            const tableBody = document.getElementById('inventory-table-body');
            tableBody.innerHTML = ''; // Clear existing rows

            products.forEach((product) => {
                const row = document.createElement('tr');
                const categoryName = categoryMap[product.category_id] || 'Unknown';

                // Check if stock quantity is below reorder level
                if (product.quantity_in_stock < product.reorder_level) {
                    alert(`Stock for ${product.product_name} is below the reorder level!`);
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
        })
        .catch((error) => {
            console.error('Error fetching inventory data:', error);
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
        });
    };

    // Trigger the API fetch and table update
    fetchAndPopulateInventory();
});
