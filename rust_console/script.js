function typeWriter(text, outputBox, delay = 30) {
    let i = 0;
    function type() {
        if (i < text.length) {
            outputBox.value += text.charAt(i);
            i++;
            setTimeout(type, delay);
        }
    }
    type();
}

async function sendInput() {
    const inputField = document.getElementById("user-input");
    const outputBox = document.getElementById("output");
    const input = inputField.value.trim();
    inputField.value = "";

    if (!input) return;

    // Type the user input first
    typeWriter("> " + input + "\n", outputBox);

    try {
        const res = await fetch("http://localhost:8000/fetch", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ url: input }),
        });

        const result = await res.text();

        // Add a short delay before printing the response
        setTimeout(() => {
            typeWriter(result + "\n", outputBox);
        }, input.length * 30 + 300); // match delay to input typing
    } catch (err) {
        setTimeout(() => {
            typeWriter("Error: " + err.message + "\n", outputBox);
        }, input.length * 30 + 300);
    }
}

// Bind to button and Enter key
document.addEventListener("DOMContentLoaded", () => {
    const button = document.getElementById("fetch-btn");
    button.addEventListener("click", sendInput);

    document.getElementById("user-input").addEventListener("keydown", (e) => {
        if (e.key === "Enter") {
            sendInput();
        }
    });
});
