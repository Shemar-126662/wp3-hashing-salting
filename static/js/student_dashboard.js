document.addEventListener("DOMContentLoaded", async function () {

    const pathParts = window.location.pathname.split("/");
    const studentId = pathParts[pathParts.length - 1];

    if (!studentId) {
        console.error("Student ID not found in URL");
        return;
    }

    try {
        const response = await fetch(`/api/students/${studentId}`);
        const data = await response.json();

        const container = document.getElementById("subjectsContainer");
        container.innerHTML = "";

        data.subjects.forEach(subject => {
            const li = document.createElement("li");
            li.classList.add("list-group-item");

            const title = document.createElement("strong");
            title.textContent = subject.name;
            li.appendChild(title);

            const innerURL = document.createElement("ul");
            innerURL.classList.add("mt-2");

            const goalsForSubject = data.learning_goals.filter(goal => goal.subject_id === subject.id);
            goalsForSubject.forEach(goal => {
                const goalLi = document.createElement("li");
                goalLi.textContent = goal.title;
                innerURL.appendChild(goalLi);
            });


            li.appendChild(innerURL);
            container.appendChild(li);
        });

    } catch (error) {
        console.error("Error loading student data:", error);
    }
});