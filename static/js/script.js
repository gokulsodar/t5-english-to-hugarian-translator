document.addEventListener("DOMContentLoaded", function () {
    const translateButton = document.querySelector(".translate-btn");
    const inputText = document.querySelector(".input-section textarea");
    const outputText = document.querySelector(".output-section textarea");
    
    translateButton.addEventListener("click", async function () {
        const textToTranslate = inputText.value.trim();
        if (!textToTranslate) {
            alert("Please enter text to translate.");
            return;
        }
        
        try {
            const apiUrl = window.location.origin + "/generate";
            const response = await fetch(apiUrl, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ text: textToTranslate })
            });
            
            if (!response.ok) {
                throw new Error("Translation request failed");
            }
            
            const data = await response.json();
            outputText.value = data.generated_text || "Translation not available";
        } catch (error) {
            console.error("Error translating text:", error);
            outputText.value = "Error occurred while translating";
        }
    });
});
