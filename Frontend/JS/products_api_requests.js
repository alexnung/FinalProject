document.addEventListener('DOMContentLoaded', () => {
    const apiUrl = 'http://127.0.0.1:5000/api/products'; // Adjust your API URL as needed

    // Fetch and populate products table
    const fetchAndPopulateProducts = async () => {
        try {
            const productsResponse = await fetch(apiUrl);
            const products = await productsResponse.json();
            const tableBody = document.querySelector('#products-table-body');
            tableBody.innerHTML = ''; // Clear existing rows

            products.forEach((product) => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${product.product_id}</td>
                    <td>${product.product_name}</td>
                    <td>${product.description}</td>
                    <td>${product.quantity_in_stock}</td>
                    <td>$${product.unit_price}</td>
                    <td>${product.category_id}</td>
                    <td>${new Date(product.created_at).toLocaleDateString()}</td>
                    <td>${new Date(product.updated_at).toLocaleDateString()}</td>
                    <td>
                        <button class="delete-product-btn" data-product-id="${product.product_id}">Delete</button>
                    </td>
                `;
                tableBody.appendChild(row);
            });

            // Add event listeners to delete buttons
            document.querySelectorAll('.delete-product-btn').forEach((button) => {
                button.addEventListener('click', async (e) => {
                    const productId = e.target.dataset.productId;
                    if (confirm(`Are you sure you want to delete product #${productId}?`)) {
                        await deleteProduct(productId);
                    }
                });
            });
        } catch (error) {
            console.error('Error fetching products:', error);
            alert('Error loading products.');
        }
    };

    // Function to delete a product
    const deleteProduct = async (productId) => {
        try {
            const response = await fetch(`${apiUrl}?product_id=${productId}`, {
                method: 'DELETE',
            });

            if (!response.ok) {
                throw new Error(`Failed to delete product: ${response.status}`);
            }

            alert('Product deleted successfully!');
            fetchAndPopulateProducts(); // Refresh the products table
        } catch (error) {
            console.error('Error deleting product:', error);
            alert('Error deleting product.');
        }
    };

    // Initialize products table on page load
    fetchAndPopulateProducts();
});
