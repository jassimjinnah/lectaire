document.addEventListener("DOMContentLoaded", function() {
    const form = document.querySelector("form");
    const videoContainer = document.getElementById("video-container");

    form.addEventListener("submit", async function(event) {
        event.preventDefault();

        const formData = new FormData(form);
        const content = formData.get("content");

        // Send AJAX request to generate video
        const response = await fetch("/generate_video", {
            method: "POST",
            body: new URLSearchParams({ content }),
            headers: {
                "Content-Type": "application/x-www-form-urlencoded"
            }
        });

        if (response.ok) {
            const videoPath = await response.text();
            const video = videoContainer.querySelector("video");
            video.src = videoPath;

            // Show the video container
            videoContainer.style.display = "block";
        } else {
            console.error("Failed to generate video.");
        }
    });
});
