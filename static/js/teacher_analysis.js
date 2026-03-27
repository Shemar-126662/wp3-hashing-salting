document.addEventListener("DOMContentLoaded", async function () {

    const response = await fetch("/api/class-learning-goals");
    const data = await response.json();

    const labels = [];
    const scores = [];

    data.forEach(goal => {
        labels.push(goal.title);
        scores.push(Math.round(goal.avg_score * 100));
    });

    const canvas = document.getElementById("learningGoalsChart");
    if (!canvas) return;

    canvas.parentElement.style.height = Math.max(labels.length * 55, 320) + "px";

    new Chart(canvas, {
        type: "bar",
        data: {
            labels: labels,
            datasets: [{
                data: scores,
                backgroundColor: "rgba(1, 77, 245, 0.75)",
                borderColor: "rgb(1, 77, 245)",
                borderWidth: 1,
                borderRadius: 6
            }]
        },
        options: {
            indexAxis: "y",
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    callbacks: {
                        label: function (context) {
                            return context.raw + "%";
                        }
                    }
                }
            },
            scales: {
                x: {
                    beginAtZero: true,
                    max: 100,
                    grid: {
                        color: "rgba(4, 31, 115, 0.08)"
                    },
                    ticks: {
                        stepSize: 20,
                        callback: function (value) {
                            return value + "%";
                        }
                    }
                },
                y: {
                    grid: {
                        display: false
                    }
                }
            }
        }
    });

});
