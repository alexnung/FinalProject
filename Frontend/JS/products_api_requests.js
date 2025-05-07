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
            const response = await fetch(`${apiUrl}/${productId}`, {
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
	
	// Submit New Product Category Form
	    addProductCategoryForm.addEventListener('submit', async (e) => {
	        e.preventDefault();

	        const categoryName = e.target.product_category_name.value;
	        const description = e.target.description.value;

	        const categoryData = {
	            category_name: categoryName,
	            description: description
	        };

	        console.log("Category data:", categoryData);

	        await createProductCategory(categoryData);
	        addProductCatModal.style.display = 'none'; // Close modal after submission
	    });
		
		// Function to create a new product category
		    const createProductCategory = async (categoryData) => {
		        try {
		            const response = await fetch('http://127.0.0.1:5000/api/product_categories', {
		                method: 'POST',
		                headers: {
		                    'Content-Type': 'application/json'
		                },
		                body: JSON.stringify(categoryData)
		            });

		            const result = await response.json();
		            if (response.ok) {
		                alert('Product category added successfully!')
		            } else {
		                alert('Error adding product category: ' + result.message);
		            }
		        } catch (error) {
		            console.error('Error creating product category:', error);
		            alert('Error creating product category.');
		        }
		    };

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

document.addEventListener('DOMContentLoaded', () => {
    const productDropdown = document.getElementById('productDropdown');
    const updateProductForm = document.getElementById('updateProductForm');
    const updateProductBtn = document.getElementById('updateProductBtn'); // Button to open the modal
    const updateProductModal = document.getElementById('updateProductModal'); // The modal element
    const cancelUpdateBtn = document.getElementById('cancelUpdateBtn'); // Button to close the modal
    const apiBaseUrl = 'http://localhost:5000/api/products'; // Update to your API URL
	const apiBaseUrl2 = 'http://localhost:5000/api/product_categories'; // Update to your API URL

    const fetchProducts = async () => {
        try {
            const response = await fetch(apiBaseUrl);
            if (!response.ok) throw new Error('Failed to fetch products');
            const products = await response.json();

            products.forEach(product => {
                const option = document.createElement('option');
                option.value = product.product_id;
                option.textContent = product.product_name;
                productDropdown.appendChild(option);
            });

            console.log('Products fetched and dropdown populated');
        } catch (error) {
            console.error('Error fetching products:', error);
        }
    };
	
	const fetchCategories = async () => {
	    try {
	        const response = await fetch(apiBaseUrl2);
	        if (!response.ok) throw new Error('Failed to fetch product categories');
	        const categories = await response.json();

	        const categoryDropdown = document.getElementById('categoryDropdown');
	        if (!categoryDropdown) throw new Error('Dropdown element not found');

	        // Clear existing options
	        categoryDropdown.innerHTML = '<option value="">Select Category</option>';

	        // Populate dropdown with categories
	        categories.forEach(category => {
	            const option = document.createElement('option');
	            option.value = category.category_id; // Set the option value to the category ID
	            option.textContent = category.category_name; // Set the display text to the category name
	            categoryDropdown.appendChild(option);
	        });

	        console.log('Categories fetched and dropdown populated');
	    } catch (error) {
	        console.error('Error fetching product categories:', error);
	    }
	};


	const populateForm = async (productId) => {
	    try {
	        const response = await fetch(`${apiBaseUrl}/${productId}`);
	        if (!response.ok) throw new Error('Failed to fetch product details');
	        const product = await response.json();

	        // Populate the form fields with product details
	        document.getElementById('productName').value = product.product_name;
	        document.getElementById('description').value = product.description;
	        document.getElementById('quantityInStock').value = product.quantity_in_stock;
	        document.getElementById('unitPrice').value = product.unit_price;
	        document.getElementById('reorderLevel').value = product.reorder_level;

	        // Populate the category dropdown
			console.log('Populating category dropdown...');
	        const categoryDropdown = document.getElementById('categoryDropdown');
	        const responseCategories = await fetch('http://127.0.0.1:5000/api/product_categories');
			console.log('Response status:', responseCategories.status);
	        if (!responseCategories.ok) throw new Error('Failed to fetch categories');
	        const categories = await responseCategories.json();
			console.log('Fetched categories:', categories);

	        // Clear the existing options in the dropdown
	        categoryDropdown.innerHTML = '';

	        // Add a default "Select Category" option
	        const defaultOption = document.createElement('option');
	        defaultOption.value = '';
	        defaultOption.textContent = 'Select Category';
	        categoryDropdown.appendChild(defaultOption);

	        // Populate the dropdown with categories
	        categories.forEach((category) => {
	            const option = document.createElement('option');
	            option.value = category.category_id;
	            option.textContent = category.category_name;
	            categoryDropdown.appendChild(option);
	        });

	        // Set the dropdown to the product's category
	        categoryDropdown.value = product.category_id;

	    } catch (error) {
	        console.error('Error fetching product details:', error);
	    }
	};




	updateProductForm.addEventListener('submit', async (e) => {
	    e.preventDefault();
	    console.log('Update product form submitted');

	    const formData = new FormData(updateProductForm);
	    const productId = productDropdown.value;

	    if (!productId) {
	        alert('Please select a product to update.');
	        return;
	    }

	    try {
	        // Fetch the current product details
	        const currentProductResponse = await fetch(`${apiBaseUrl}/${productId}`);
	        if (!currentProductResponse.ok) throw new Error('Failed to fetch current product details');
	        const currentProduct = await currentProductResponse.json();

	        // Prepare the payload with existing values as fallback if fields are left blank
	        const payload = {
	            product_name: formData.get('product_name') || currentProduct.product_name,  // Use existing if blank
	            description: formData.get('description') || currentProduct.description,  // Use existing if blank
	            quantity_in_stock: formData.get('quantity_in_stock') || currentProduct.quantity_in_stock,  // Use existing if blank
	            unit_price: formData.get('unit_price') || currentProduct.unit_price,  // Use existing if blank
	            reorder_level: formData.get('reorder_level') || currentProduct.reorder_level,  // Use existing if blank
	            category_id: formData.get('category_id') || currentProduct.category_id,  // Use existing if blank
	        };

	        // Prepare the payload with non-empty fields only
	        const filteredPayload = {};
	        for (const key in payload) {
	            if (payload[key] !== '' && payload[key] !== null && payload[key] !== undefined) {
	                filteredPayload[key] = payload[key];
	            }
	        }

	        // Send the update request
	        const response = await fetch(`${apiBaseUrl}/${productId}`, {
	            method: 'PUT',
	            headers: { 'Content-Type': 'application/json' },
	            body: JSON.stringify(filteredPayload),
	        });

	        if (!response.ok) throw new Error('Failed to update product');
	        alert('Product updated successfully');
	        updateProductModal.style.display = 'none'; // Close modal after successful update
	        console.log('Product updated:', productId);
	    } catch (error) {
	        console.error('Error updating product:', error);
	        alert('Failed to update product');
	    }
	});




    productDropdown.addEventListener('change', () => {
        const selectedProductId = productDropdown.value;
        if (selectedProductId) {
            console.log('Product selected:', selectedProductId);
            populateForm(selectedProductId);
        }
    });

    // Show Update Product Modal
    updateProductBtn.addEventListener('click', () => {
        updateProductModal.style.display = 'flex';
        console.log('Update Product Modal opened');
    });

    // Close Update Product Modal
    cancelUpdateBtn.addEventListener('click', () => {
        updateProductModal.style.display = 'none';
        console.log('Update Product Modal closed');
    });

    fetchProducts();
	fetchCategories();
});


