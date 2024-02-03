document.getElementById("textForm").addEventListener("submit", function (event) {
    event.preventDefault();
    const textData = document.getElementById("text").value;
    if ([...textData].length > 100) {
        alert("Above byte limit: 100!")
        return
    }

    fetch("/new-share", {
        method: "POST",
        body: textData
    })
    .then(response => response.text())  // Parse the response as plain text
    .then(data => {
        alert(`Share UUID: ${data}`);
    })
    .catch(error => console.error("Error:", error));
});
