function handleEnter(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault(); // prevent newline
        document.getElementById('message-form').submit(); // submit the form
    }
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
    var submitButton = document.getElementById("submit-button");
    var loadingIndicator = document.getElementById("loading-indicator");
    form.onsubmit = function() {
        submitButton.disabled = true;
        submitButton.style.display = "none";
        loadingIndicator.style.display = "block";
    };

    var submitButton = document.getElementById("submit-button");
    if (submitButton) {
      submitButton.addEventListener('click', function() {
        submitButton.disabled = true;
      });
    }
});