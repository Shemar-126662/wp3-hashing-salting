document.addEventListener("DOMContentLoaded", async function () {

    const learningGoalId = window.learningGoalId;

    const response = await fetch(`/api/students/${studentId}/learning-goal/${learningGoalId}`);
    const data = await response.json();

    const labels = data.map(d => d.level);

    const kennen = data.map(d => Math.round(d.kennen * 100));
    const kunnen = data.map(d => Math.round(d.kunnen * 100));
    const confidence = data.map(d => Math.round(d.confidence * 100));

    new Chart(document.getElementById("taxonomyChart"), {
        type: "bar",
        data: {
            labels: labels,
            datasets: [
                {
                    label: "Kennen",
                    data: kennen,
                },
                {
                    label: "Kunnen",
                    data: kunnen,
                },
                {
                    label: "Confidence",
                    data: confidence,
                }
            ]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100
                }
            }
        }
    });
});
        