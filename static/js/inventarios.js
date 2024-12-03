// Inventarios JS
document.getElementById("filterButton").addEventListener("click", function() {
    const searchTerm = document.getElementById("searchInput").value.toLowerCase();
    const rows = document.querySelectorAll(".inventory-table tbody tr");
    rows.forEach(row => {
        const itemName = row.cells[0].textContent.toLowerCase();
        if (itemName.includes(searchTerm)) {
            row.style.display = "";
        } else {
            row.style.display = "none";
        }
    });
});
