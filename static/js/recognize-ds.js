const startBtn = document.getElementById('start-btn');
const output = document.getElementById('chatbox');
let recognition;
let isListening = false;

// Check for browser support
if ('SpeechRecognition' in window || 'webkitSpeechRecognition' in window) {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    recognition = new SpeechRecognition();
    // Configure recognition settings
    recognition.continuous = true;
    recognition.interimResults = true;
    recognition.lang = 'en-US';
    let x = 0;
    // Event handlers
    recognition.onresult = (event) => {
        let transcript = '';
        for (let i = event.resultIndex; i < event.results.length; i++) {
            let speech = event.results[i][0].transcript;
            if (event.results[i].isFinal) {
                transcript += speech;
            } else {
                // transcript += speech + ' (processing...)';
                transcript += speech;
            }
        }
        // alert(transcript);
        if (transcript.toLowerCase().includes("go") || transcript.toLowerCase().includes("enter") || transcript.toLowerCase().includes("submit")) {
            transcript = transcript.replace(/go|enter|submit/gi, '').trim();
            // alert(transcript);
            if (transcript == '' || transcript == '(processing...)')
                // alert('Empty..');
                console.log("Empty");
            else {
                isListening = false;
                recognition.stop();
                // stopListening();
            }
        }
        output.value = transcript;
    };

    recognition.onerror = (event) => {
        console.error('Speech recognition error:', event.error);
        isListening = false;
        recognition.stop();
    };

    // Event: When recognition.stop() call..
    recognition.onend = () => {
        // alert("H-onend" + output.value);
        if (isListening) {
            recognition.start();
        }
        else {
            // console.info('Back End Code..');
            // alert('Back End Calling...')
            call_back_end();
            isListening = false;
            output.value = '';
            output.placeholder = "Ask me anything.";
            startBtn.classList.remove("active");
            output.classList.remove("myplaceholder");
        }
    };

    startBtn.addEventListener('click', () => {
        if (!isListening) {
            startListening();
        } else {
            stopListening();
        }
    });
}
else {
    // startBtn.disabled = true;
    output.value = 'Speech recognition not supported in this browser.';
}

function startListening() {
    recognition.start();
    isListening = true;
    output.placeholder = "Start Listening...";
    startBtn.classList.add("active");
    output.classList.add("myplaceholder");
}

function stopListening() {
    recognition.stop();
    isListening = false;
    output.value = '';
    output.placeholder = "Ask me anything.";
    startBtn.classList.remove("active");
    output.classList.remove("myplaceholder");
    // alert("function stopListening()");
}