
let allData = [];

document.addEventListener("DOMContentLoaded", async function () {

    const response = await fetch(`/api/students/${window.studentId}/snapshots`);
    if (!response.ok) { console.error('API error', response.status); return; }

    allData = await response.json();
    renderTable(allData);
    initFilters(allData);
});

function renderTable(data) {
    const table = document.getElementById("snapshotsTable");
    table.innerHTML = "";

    const grouped = {};

    data.forEach(row => {
        const key = row.title + row.date;
        if (!grouped[key]) {
            grouped[key] = {
                title: row.title,
                source: row.source_type,
                date: row.date,
                keywords: row.keywords,
                levels: {}
            };
        }
        grouped[key].levels[row.level] = Math.round(row.avg_score * 100);
    });

    Object.values(grouped).forEach(item => {
        const tr = document.createElement("tr");

        tr.innerHTML = `
            <td>${item.title}</td>
            <td>${item.source}</td>
            <td>${item.date}</td>
            <td>${item.keywords || ''}</td>
            <td>${item.levels["Onthouden"] || 0}</td>
            <td>${item.levels["Begrijpen"] || 0}</td>
            <td>${item.levels["Toepassen"] || 0}</td>
            <td>${item.levels["Analyseren"] || 0}</td>
        `;
        table.appendChild(tr);
    });
}

function initFilters(data) {
    const titles = [...new Set(data.map(d => d.title))];
    const sources = [...new Set(data.map(d => d.source_type))];

    const titleSelect = document.getElementById("filterTitle");
    const sourceSelect = document.getElementById("filterSource");

    titles.forEach(title => {
        titleSelect.innerHTML += `<option value="${title}">${title}</option>`;
    });

    sources.forEach(s => {
        sourceSelect.innerHTML += `<option value="${s}">${s}</option>`;
    });

    titleSelect.addEventListener("change", applyFilters);
    sourceSelect.addEventListener("change", applyFilters);
    document.getElementById("filterDate").addEventListener("change", applyFilters);
    document.getElementById("resetFilters").addEventListener("click", resetFilters);
}

function applyFilters() {
    const title = document.getElementById("filterTitle").value;
    const source = document.getElementById("filterSource").value;
    const date = document.getElementById("filterDate").value;

    let filtered = allData;

    if (title) {
        filtered = filtered.filter(d => d.title === title);
    }
    if (source) {
        filtered = filtered.filter(d => d.source_type === source);
    }
    if (date) {
        filtered = filtered.filter(d => d.date === date);
    }

    renderTable(filtered);
}

function resetFilters() {
    document.getElementById("filterTitle").value = "";
    document.getElementById("filterSource").value = "";
    document.getElementById("filterDate").value = "";
    renderTable(allData);
}
