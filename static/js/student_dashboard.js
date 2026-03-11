document.addEventListener("DOMContentLoaded", async function () {
    let studentId = window.studentId;

    if (!studentId) {
        console.error("Student ID not found in URL");
        return;
    }

    try {
        const response = await fetch("/api/students/" + studentId);
        const data = await response.json();

        
        const container = document.getElementById("subjectsContainer");
        if (!container) return;

        const progressMap = {};
        for (let i = 0; i < data.progress_data.length; i++) {
            const progress = data.progress_data[i];
            const avg = (progress.avg_kennen + progress.avg_kunnen) / 2;
            progressMap[progress.lg_id] = Math.round(avg * 100);
        }

        for (let i = 0; i < data.subjects.length; i++) {
            const subject = data.subjects[i];
            
            const goalsForSubject = [];
            for (let j = 0; j < data.learning_goals.length; j++) {
                if (data.learning_goals[j].subject_id === subject.id) {
                    goalsForSubject.push(data.learning_goals[j]);
                }
            }

            if (goalsForSubject.length === 0) continue;

            const div = document.createElement("div");

            const title = document.createElement("strong");
            title.textContent = subject.name;
            div.appendChild(title);
            const chartDiv = document.createElement("div");
            chartDiv.style.width = "100%";
            chartDiv.style.height = "350px";
            div.appendChild(chartDiv);

            const canvas = document.createElement("canvas");
            canvas.id = "chart-" + subject.id;
            chartDiv.appendChild(canvas);

            const labels = [];
            const values = [];
            for (let j = 0; j < goalsForSubject.length; j++) {
                const goal = goalsForSubject[j];
                labels.push(goal.title);
                values.push(progressMap[goal.id] || 0);
            }

            new Chart(canvas, {
                type: "bar",
                data: {
                    labels: labels,
                    datasets: [{
                        data: values
                    }]
                },
                options: {
                    indexAxis: "y",
                    responsive: true,
                    maintainAspectRatio: false
                }
            });

            container.appendChild(div);
        }

    } catch (error) {
        console.error("Error loading student data:", error);
    }
}); 