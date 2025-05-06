document.addEventListener('DOMContentLoaded', () => {
    const fetchAndPopulateProducts = () => {
        fetch('http://127.0.0.1:5000/api/products')
            .then((response) => {
                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }
                return response.json();
            })
            .then((products) => {
                console.log('API Response:', products); // Log response for debugging

                const tableBody = document.getElementById('products-table-body');
                tableBody.innerHTML = ''; // Clear existing rows

                products.forEach((product) => {
                    const row = document.createElement('tr');

                    const unitPrice = isNaN(product.unit_price)
                        ? 0
                        : parseFloat(product.unit_price).toFixed(2);

                    row.innerHTML = `
                        <td>${product.product_id}</td>
                        <td>${product.product_name}</td>
                        <td>${product.description}</td>
                        <td>${product.quantity_in_stock}</td>
                        <td>$${unitPrice}</td>
                        <td>${product.category_id}</td>
                        <td>${new Date(product.created_at).toLocaleDateString()}</td>
                        <td>${new Date(product.updated_at).toLocaleDateString()}</td>
                    `;

                    tableBody.appendChild(row);
                });
            })
            .catch((error) => {
                console.error('Error fetching products:', error);
                const tableBody = document.getElementById('products-table-body');
                if (tableBody) {
                    tableBody.innerHTML = `
                        <tr>
                            <td colspan="8" style="text-align: center; color: red;">
                                Failed to load products. Please try again later.
                            </td>
                        </tr>
                    `;
                }
            });
    };

    // Trigger the API fetch and table update
    fetchAndPopulateProducts();
});
