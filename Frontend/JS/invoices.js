document.addEventListener('DOMContentLoaded', () => {
    const fetchAndPopulateInvoices = () => {
        fetch('http://127.0.0.1:5000/api/invoices') // Adjust the endpoint as needed
            .then((response) => {
                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }
                return response.json();
            })
            .then((invoices) => {
                console.log('Fetched Invoices:', invoices); // Debugging purpose
                const tableBody = document.querySelector('tbody');
                tableBody.innerHTML = ''; // Clear existing rows

                invoices.forEach((invoice) => {
                    const row = document.createElement('tr');

                    row.innerHTML = `
                        <td>${invoice.formatted_invoice_id}</td>
                        <td>${invoice.customer_id}</td>
                        <td>${new Date(invoice.invoice_date).toLocaleDateString()}</td>
                        <td>${invoice.payment_status}</td>
                        <td>$${parseFloat(invoice.total_amount).toFixed(2)}</td>
                    `;

                    tableBody.appendChild(row);
                });
            })
            .catch((error) => {
                console.error('Error fetching invoices:', error);

                const tableBody = document.querySelector('tbody');
                tableBody.innerHTML = `
                    <tr>
                        <td colspan="5" style="text-align: center; color: red;">
                            Failed to load invoices. Please try again later.
                        </td>
                    </tr>
                `;
            });
    };

    // Call the function to fetch and populate invoices
    fetchAndPopulateInvoices();
});
