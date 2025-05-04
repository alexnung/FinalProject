document.addEventListener("DOMContentLoaded", () => {
    const searchTable = (tableClass, searchInputClass) => {
        const input = document.querySelector(`.${searchInputClass}`).value.toLowerCase();
        const table = document.querySelector(`.${tableClass}`);
        const rows = table.getElementsByTagName('tr');

        for (let i = 1; i < rows.length; i++) { // Skip header row
            const cells = rows[i].getElementsByTagName('td');
            let match = false;

            for (let j = 0; j < cells.length; j++) {
                if (cells[j] && cells[j].textContent.toLowerCase().includes(input)) {
                    match = true;
                    break;
                }
            }

            rows[i].style.display = match ? '' : 'none';
        }
    };

    // Attach the searchTable function to the search input
    const searchInput = document.querySelector('.searchBar'); // Use class selector
    searchInput.addEventListener('keyup', () => {
        searchTable('results-table', 'searchBar'); // Use class names here
    });
});
