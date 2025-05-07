document.addEventListener('DOMContentLoaded', () => {
    const apiReportsUrl = 'http://127.0.0.1:5000/api/reports';
    const apiUsersUrl = 'http://127.0.0.1:5000/api/users';

    // Fetch and populate reports table
    const fetchAndPopulateReports = async () => {
        try {
            // Fetch reports
            const reportsResponse = await fetch(apiReportsUrl);
            if (!reportsResponse.ok) {
                throw new Error(`HTTP error! Status: ${reportsResponse.status}`);
            }
            const reports = await reportsResponse.json();

            // Fetch users
            const usersResponse = await fetch(apiUsersUrl);
            if (!usersResponse.ok) {
                throw new Error(`HTTP error! Status: ${usersResponse.status}`);
            }
            const users = await usersResponse.json();

            // Map user_id to username
            const userMap = {};
            users.forEach((user) => {
                userMap[user.user_id] = user.username;
            });

            // Populate table
            const tableBody = document.querySelector('#reports-table-body');
            tableBody.innerHTML = ''; // Clear existing rows

            reports.forEach((report) => {
                const row = document.createElement('tr');

                // Format `report_data` as plain text
                const formattedReportData = Object.entries(JSON.parse(report.report_data || '{}'))
                    .map(([key, value]) => {
                        const formattedKey = key
                            .split('_')
                            .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
                            .join(' ');
                        return `${formattedKey}: ${value}`;
                    })
                    .join(', ');

                row.innerHTML = `
                    <td>${report.report_id}</td>
                    <td>${report.report_type}</td>
                    <td>${new Date(report.generated_at).toLocaleDateString()} ${new Date(report.generated_at).toLocaleTimeString()}</td>
                    <td>${userMap[report.user_id] || 'Unknown User'}</td>
                    <td>${formattedReportData || 'No Data'}</td>
                    <td>
                        <button class="delete-report-btn" data-report-id="${report.report_id}">Delete</button>
                    </td>
                `;

                tableBody.appendChild(row);
            });

            // Add event listeners to delete buttons
            document.querySelectorAll('.delete-report-btn').forEach((button) => {
                button.addEventListener('click', async (e) => {
                    const reportId = e.target.dataset.reportId;
                    if (confirm(`Are you sure you want to delete report #${reportId}?`)) {
                        await deleteReport(reportId);
                    }
                });
            });
        } catch (error) {
            console.error('Error fetching reports:', error);

            const tableBody = document.querySelector('#reports-table-body');
            tableBody.innerHTML = `
                <tr>
                    <td colspan="6" style="text-align: center; color: red;">
                        Failed to load reports. Please try again later.
                    </td>
                </tr>
            `;
        }
    };

    // Function to delete a report
    const deleteReport = async (reportId) => {
        try {
            const response = await fetch(`${apiReportsUrl}/${reportId}`, {
                method: 'DELETE',
            });

            if (!response.ok) {
                throw new Error(`Failed to delete report: ${response.status}`);
            }

            alert('Report deleted successfully!');
            fetchAndPopulateReports(); // Refresh the reports table
        } catch (error) {
            console.error('Error deleting report:', error);
            alert('Error deleting report.');
        }
    };

    // Initialize reports table on page load
    fetchAndPopulateReports();
});
