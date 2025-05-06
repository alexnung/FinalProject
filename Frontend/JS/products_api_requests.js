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

document.addEventListener('DOMContentLoaded', () => {
    const createProductCatBtn = document.getElementById('createProductCatBtn');
    const createProductBtn = document.getElementById('createProductBtn');
    const addProductCatModal = document.getElementById('addProductCatModal');
    const addProductModal = document.getElementById('addProductModal');
    const cancelCategoryBtn = document.getElementById('cancelCategoryBtn');
    const cancelProductBtn = document.getElementById('cancelProductBtn');
	
    // Show New Product Category Modal
    createProductCatBtn.addEventListener('click', () => {
        addProductCatModal.style.display = 'flex';
    });

    // Show New Product Modal
    createProductBtn.addEventListener('click', () => {
        addProductModal.style.display = 'flex';
        populateCategoryDropdown(); // Populate the category dropdown
    });

    // Close New Product Category Modal
    cancelCategoryBtn.addEventListener('click', () => {
        addProductCatModal.style.display = 'none';
    });

    // Close New Product Modal
    cancelProductBtn.addEventListener('click', () => {
        addProductModal.style.display = 'none';
    });

    // Fetch and populate category dropdown for New Product Form
	const populateCategoryDropdown = async () => {
	    console.log("Fetching categories...");
	    try {
	        const response = await fetch('http://127.0.0.1:5000/api/product_categories');
	        console.log('Response status:', response.status);  // Log status

	        if (!response.ok) {
	            console.error('Failed to fetch categories:', response.statusText);
	            alert('Failed to load categories.');
	            return;
	        }

	        const categories = await response.json();
	        console.log('Categories data:', categories);  // Log the categories data

	        const categorySelect = document.getElementById('categoryName');
			console.log('Category select element:', categorySelect);
	        categorySelect.innerHTML = ''; // Clear existing options first

	        // Add a default "Select Category" option
	        const defaultOption = document.createElement('option');
	        defaultOption.value = '';
	        defaultOption.textContent = 'Select Category';
	        categorySelect.appendChild(defaultOption);

	        // Populate dropdown with categories
	        categories.forEach((category) => {
	            const option = document.createElement('option');
	            option.value = category.category_id;  // Set value to category ID
	            option.textContent = category.category_name;  // Display category name
	            categorySelect.appendChild(option);
				
				console.log('Appended option:', option);
	        });
	    } catch (error) {
	        console.error('Error fetching categories:', error);
	        alert('Error fetching categories.');
	    }
	};


    // Submit New Product Form
    document.getElementById('addProductForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        const data = {
            product_name: e.target.product_name.value,
            description: e.target.description.value,
            quantity_in_stock: e.target.quantity_in_stock.value,
            unit_price: e.target.unit_price.value,
			reorder_level: e.target.reorder_level.value,
            category_id: e.target.category_id.value
        };
		

        console.log("Product data:", data);

        await createProduct(data);
        addProductModal.style.display = 'none'; // Close modal after form submission
    });

    // Function to create a new product
    const createProduct = async (data) => {
        try {
            const response = await fetch('http://127.0.0.1:5000/api/products', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            });

            const result = await response.json();
            if (response.ok) {
                alert('Product added successfully!');
            } else {
                alert('Error adding product: ' + result.message);
            }
        } catch (error) {
            console.error('Error creating product:', error);
            alert('Error creating product.');
        }
    };
});

