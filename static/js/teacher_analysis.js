document.addEventListener("DOMContentLoaded", async function () {

    const response = await fetch("/api/class-learning-goals");
    const data = await response.json();

    const labels = [];
    const scores = [];

    data.forEach(goal => {
        labels.push(goal.title);
        scores.push(Math.round(goal.avg_score * 100));
    });

    new Chart(document.getElementById("learningGoalsChart"), {
        type: "bar",
        data: {
            labels: labels,
            datasets: [{
                label: "Average Score (%)",
                data: scores
            }]
        },
        options: {
            indexAxis: "y",
        }
    });

});