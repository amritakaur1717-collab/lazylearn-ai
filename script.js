const notesInput = document.getElementById("notes");
const taskSelect = document.getElementById("task");
const generateBtn = document.getElementById("generateBtn");
const resultCard = document.getElementById("resultCard");
const resultTitle = document.getElementById("resultTitle");
const result = document.getElementById("result");

const taskTitles = {
    summary: "✨ Your Smart Summary",
    questions: "❓ Important Questions",
    flashcards: "🗂️ Your Flashcards",
    quiz: "🧠 Practice Quiz",
    explain: "💡 Simple Explanation"
};

generateBtn.addEventListener("click", async () => {
    const notes = notesInput.value.trim();
    const task = taskSelect.value;

    if (!notes) {
        alert("Please paste your study notes first!");
        notesInput.focus();
        return;
    }

    resultCard.hidden = false;
    resultTitle.textContent = taskTitles[task];
    result.textContent = "Preparing your study material...";
    generateBtn.disabled = true;
    generateBtn.textContent = "Please wait...";

    try {
        const response = await fetch("/api/study", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ notes, task })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Something went wrong.");
        }

        result.textContent = data.result;
    } catch (error) {
        result.textContent =
            "Your study assistant needs its AI connection to be set up. " +
            "Save your work—we will connect the open-source AI model next!";
        console.error(error);
    } finally {
        generateBtn.disabled = false;
        generateBtn.textContent = "Generate with AI ↗";
    }
});