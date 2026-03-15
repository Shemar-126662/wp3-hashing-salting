document.addEventListener("DOMContentLoaded", async function () {

    try {
        const response = await fetch("/api/class-overview");
        const data = await response.json();

        const labels = [];
        const scores = [];

        data.forEach(student => {
            labels.push(student.name);
            scores.push(Math.round(student.avg_score * 100));
        });

        const ctx = document.getElementById("classChart");

        new Chart(ctx, {
            type: "bar",
            data: {
                labels: labels,
                datasets: [{
                    label: "Average Score (%)",
                    data: scores
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        display: false
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 100
                    }
                }
            }
        });

    } catch (error) {
        console.error("Error loading class overview:", error);
    }

});