document.addEventListener("DOMContentLoaded", async function () {

    const response = await fetch(`/api/students/${window.studentId}/snapshots`);
    if (!response.ok) { console.error('API error', response.status); return; }
    const data = await response.json();
    console.log('Snapshots data:', data);

    const table = document.getElementById("snapshotsTable");

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
});
