function handleEnter(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        submitForm();
    }
}

function submitForm() {
    var messageBox = document.querySelector(".user-msgbox");
    messageBox.classList.add('disabled-text-effect');
    // apply effect also to any buttons for challenge & lesson accepts
    document.getElementById('message-form').submit();
}

function resizeTextarea() {
    var textarea = document.querySelector(".user-msgbox");
    if (textarea) {
        textarea.style.height = "auto";
        textarea.style.height = (textarea.scrollHeight) + "px";
    }
}

document.addEventListener("DOMContentLoaded", function() {
    var textarea = document.querySelector(".user-msgbox");
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

// DARK/LIGHT
function toggleLightMode() {
    document.body.classList.toggle('light-mode');
    var btn = document.getElementById("light-mode-toggle");

    // Save the current mode to localStorage
    if (document.body.classList.contains('light-mode')) {
        localStorage.setItem('mode', 'light');
        btn.value = "Dark mode"
    } else {
        localStorage.setItem('mode', 'dark');
        btn.value = "Light mode"
    }
}
// Apply dark/light mode from localStorage when the page loads
document.addEventListener("DOMContentLoaded", function() {
    var mode = localStorage.getItem('mode');
    if (mode === 'light') {
        document.body.classList.add('light-mode');
    }
});

// LESSON & CHALLENGE

function handleChallenge(challenge) {
    changeUserText("Accept challenge: " + challenge);
    submitForm();
}

function handleLesson(lesson) {
    changeUserText("Start lesson: " +  lesson);
    submitForm();
}

function changeUserText(desiredText) {
    var textarea = document.querySelector('.user-msgbox');
    textarea.value = desiredText;
}