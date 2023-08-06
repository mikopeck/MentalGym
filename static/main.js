function handleEnter(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault(); // prevent newline
        submitForm(); // unified form submission handling
    }
}

function submitForm() {
    var submitButton = document.getElementById("submit-button");
    var loadingIndicator = document.getElementById("loading-indicator");
    submitButton.style.display = "none";
    loadingIndicator.style.display = "block";
    document.getElementById('message-form').submit();
}

function resizeTextarea() {
    var textarea = document.querySelector(".invisible-field");
    if (textarea) {
        textarea.style.height = "auto";
        textarea.style.height = (textarea.scrollHeight) + "px";
    }
}

// Attach the resizeTextarea function to the input event of the textarea
document.addEventListener("DOMContentLoaded", function() {
    var textarea = document.querySelector(".invisible-field");
    if (textarea) {
        textarea.addEventListener("input", resizeTextarea);
        resizeTextarea();
    }

    // Scroll to the bottom of the conversation
    var conversationDiv = document.getElementById("conversation");
    if (conversationDiv) {
        conversationDiv.scrollTop = conversationDiv.scrollHeight;
    }

    // Handle form submission
    var form = document.getElementById("message-form");
    form.onsubmit = function(e) {
        e.preventDefault();
        submitForm();
    };
});


    function toggleLightMode() {
        document.body.classList.toggle('light-mode');
        // Save the current mode to localStorage
        if (document.body.classList.contains('light-mode')) {
            localStorage.setItem('mode', 'light');
        } else {
            localStorage.setItem('mode', 'dark');
        }
    
}
// Apply dark/light mode from localStorage when the page loads
document.addEventListener("DOMContentLoaded", function() {
    var mode = localStorage.getItem('mode');
    if (mode === 'light') {
        document.body.classList.add('light-mode');
    }
});
