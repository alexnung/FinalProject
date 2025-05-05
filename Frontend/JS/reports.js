document.addEventListener('DOMContentLoaded', () => {
    const fetchAndPopulateReports = async () => {
        try {
            // Fetch reports
            const reportsResponse = await fetch('http://127.0.0.1:5000/api/reports');
            if (!reportsResponse.ok) {
                throw new Error(`HTTP error! Status: ${reportsResponse.status}`);
            }
            const reports = await reportsResponse.json();

            // Fetch users
            const usersResponse = await fetch('http://127.0.0.1:5000/api/users');
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
            const tableBody = document.querySelector('tbody');
            tableBody.innerHTML = ''; // Clear existing rows

            reports.forEach((report) => {
                const row = document.createElement('tr');

                // Format `report_data` as plain text
                const formattedReportData = Object.entries(JSON.parse(report.report_data || '{}'))
                    .map(([key, value]) => {
                        // Capitalize keys and format them
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
                `;

                tableBody.appendChild(row);
            });
        } catch (error) {
            console.error('Error fetching reports:', error);

            const tableBody = document.querySelector('tbody');
            tableBody.innerHTML = `
                <tr>
                    <td colspan="5" style="text-align: center; color: red;">
                        Failed to load reports. Please try again later.
                    </td>
                </tr>
            `;
        }
    };

    // Call the function to fetch and populate reports
    fetchAndPopulateReports();
});
