document.getElementById("textForm").addEventListener("submit", function (event) {
    event.preventDefault();
    const formData = new FormData();
    const textData = document.getElementById("text").value;

    // Add the text data as a Blob with 'text/plain' content type
    const blob = new Blob([textData], { type: "text/plain" });

    // Append the Blob to the FormData with the field name "file"
    formData.append("file", blob, "text_data.txt");

    fetch("/new-share", {
        method: "POST",
        body: formData
    })
    .then(response => response.text())  // Parse the response as plain text
    .then(data => {
        alert(`Share UUID: ${data}`);
    })
    .catch(error => console.error("Error:", error));
});
