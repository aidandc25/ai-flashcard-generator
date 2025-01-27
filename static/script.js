document.getElementById("generate-btn").addEventListener("click", async () => {
    const inputTopic = document.getElementById("topic").value;
    const flashcardsContainer = document.getElementById("flashcards");
    const responseMessage = document.getElementById("response");

    // Clear previous results and show the loading circle
    flashcardsContainer.innerHTML = "";
    responseMessage.style.color = "green";
    responseMessage.innerHTML = `<div class="loading-circle"></div>`;

    try {
        const response = await fetch("/generate", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ topic: inputTopic })
        });

        const data = await response.json();

        if (!response.ok) {
            responseMessage.style.color = "red";
            responseMessage.innerHTML = data.error || "An error occurred. Please try again.";
            return;
        }

        responseMessage.innerHTML = "";
        if (data.flashcards && data.flashcards.length > 0) {
            flashcardsContainer.innerHTML = data.flashcards.map(flashcard => `
                <div class="card">
                    <p><strong>Q:</strong> ${flashcard.question}</p>
                    <p><strong>A:</strong> ${flashcard.answer}</p>
                </div>
            `).join("");
        } else {
            flashcardsContainer.innerHTML = "<p>No flashcards generated.</p>";
        }
    } catch (error) {
        console.error("Error:", error);
        responseMessage.style.color = "red";
        responseMessage.innerHTML = "An error occurred. Please try again.";
    }
});
