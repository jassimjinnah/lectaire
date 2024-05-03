let mediaRecorder;
let chunks = [];

// Function to start recording
function startRecording() {
    navigator.mediaDevices.getUserMedia({ audio: true })
        .then(function(stream) {
            mediaRecorder = new MediaRecorder(stream);
            mediaRecorder.ondataavailable = function(event) {
                chunks.push(event.data);
            };
            mediaRecorder.start();
        })
        .catch(function(err) {
            console.error('Error accessing microphone: ', err);
        });
}

// Function to stop recording
function stopRecording() {
    if (mediaRecorder && mediaRecorder.state === 'recording') {
        mediaRecorder.stop();
    }
}

// Function to download recorded audio
function downloadRecording() {
    if (chunks.length === 0) {
        console.error('No audio recorded');
        return;
    }

    const blob = new Blob(chunks, { type: 'audio/webm' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'recording.webm';
    document.body.appendChild(a);
    a.click();
    URL.revokeObjectURL(url);
}

// Event listener to handle start recording button click
document.getElementById('startRecord').addEventListener('click', startRecording);

// Event listener to handle stop recording button click
document.getElementById('stopRecord').addEventListener('click', stopRecording);

// Event listener to handle download recording button click
document.getElementById('downloadRecord').addEventListener('click', downloadRecording);
