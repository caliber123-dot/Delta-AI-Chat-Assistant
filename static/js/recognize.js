// Check browser support for SpeechRecognition
const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

if (SpeechRecognition) {
    const recognition = new SpeechRecognition();
    const startButton = document.getElementById('start-btn');
    const transcriptOutput = document.getElementById('chatbox');
    const statusOutput = document.getElementById('status');

    // Set recognition settings
    recognition.lang = 'en-US'; // Set the language
    recognition.interimResults = true; // Show results while speaking
    recognition.continuous = true; // Keep listening until stopped

    let x = 0;
    // Event: When speech is recognized
    recognition.onresult = (event) => {
        let transcript = '';
        for (const result of event.results) {
            let speech = result[0].transcript;
            if (speech.toLowerCase().includes("go") || speech.toLowerCase().includes("enter") || speech.toLowerCase().includes("submit")) {
                speech = speech.replace(/go|enter|submit/gi, '').trim();
                if (x === 0) {
                    recognition.stop();
                    x = x + 1;
                }
                else if (x === 1) {
                    // Fianal Submit                   
                    x = x + 1;
                }
            }
            transcript += speech;
            // const match = transcript.toLowerCase().match(/remove\s+(\w+)/); // Match "remove <word>"
            // if (match) {
            //     const wordToRemove = match[1]; // Extract the word to remove
            //     const removeRegex = new RegExp(`\\b${wordToRemove}\\b`, "gi"); // Create regex to remove the word
            //     // speech = speech.replace(removeRegex, '').trim(); // Remove the word
            //     transcript = transcript.replace(removeRegex, '').replace(/remove\s+\w+/, '').trim();
            // }
        }
        transcriptOutput.value = transcript.trim();
    };

    // Event: When recognition starts
    recognition.onstart = () => {
        // alert("Status: Listening...");
        console.log("Status: Listening...");
    };

    // Event: When recognition stops
    recognition.onend = () => {
        // alert("Status: Stop Listening !!!");
        call_back_end();
        transcriptOutput.value = '';
        transcriptOutput.placeholder = "Ask me anything.";
        startButton.classList.remove("active");
        isListening = false;

        transcriptOutput.classList.remove("myplaceholder");
    };

    // Event: On error
    recognition.onerror = (event) => {
        console.error('Speech Recognition Error:', event.error);
        var err = `Error: ${event.error}`;
        console.log(err);
        // alert(err);
    };

    // Toggle recognition with button
    let isListening = false;
    startButton.addEventListener('click', () => {
        if (isListening) {
            recognition.stop();
            transcriptOutput.value = '';
            transcriptOutput.placeholder = "Ask me anything.";
            startButton.classList.remove("active");
            transcriptOutput.classList.remove("myplaceholder");
        } else {
            recognition.start();
            x = 0;
            transcriptOutput.placeholder = "Start Listening...";
            startButton.classList.add("active");
            transcriptOutput.classList.add("myplaceholder");
        }
        isListening = !isListening;
    });
} else {
    alert('Speech Recognition is not supported in this browser. Please use Chrome or Edge.');
}

