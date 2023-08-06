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

document.addEventListener("DOMContentLoaded", function() {
    // Focus the textarea
    var textarea = document.querySelector(".invisible-field");
    if (textarea) {
        textarea.focus();
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
}