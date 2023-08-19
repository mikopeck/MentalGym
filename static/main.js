function handleEnter(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        e.stopPropagation();
        submitForm();
    }
}

function submitForm() {
    var messageBox = document.querySelector(".user-msgbox");
    messageBox.classList.add('disabled-text-effect');
    messageBox.disabled = true;
    // todo: apply effect also to any buttons for challenge & lesson accepts

    var formData = new FormData();
    formData.append("message", messageBox.value);

    var xhr = new XMLHttpRequest();

    xhr.open("POST", "/", true);
    xhr.onreadystatechange = function () {
        if (xhr.readyState == 4 && xhr.status == 200) {
            var response = JSON.parse(xhr.responseText);

            // Update the page
            // Actions
            var rightSection = document.querySelector(".right-section");
            rightSection.innerHTML = '';
            response.actions.forEach(function(action) {
                var button = document.createElement("button");
                button.id = "action-btn";
                button.className = "fade-in";
                button.onclick = function() { handleAction(action); };

                var img = document.createElement("img");
                img.src = "/Images/TopicChoosing2.png";
                img.className = "icon";
                button.appendChild(img);

                var text = document.createTextNode(action);
                button.appendChild(text);

                rightSection.appendChild(button);
            });
            // Conversation
            var conversationDiv = document.getElementById("conversation");
            conversationDiv.innerHTML = '';
            response.messages.forEach(function(message) {
                if (message.role != 'system') {
                    var div = document.createElement("div");
                    div.className = message.role + " fade-in";
                    var p = document.createElement("p");
                    p.textContent = message.content;
                    div.appendChild(p);
                    conversationDiv.appendChild(div);
                }
            });
            conversationDiv.scrollTop = conversationDiv.scrollHeight;
            // MessageBox
            messageBox.value = '';
            resizeTextarea();
            messageBox.classList.remove('disabled-text-effect');
            messageBox.disabled = false;
            messageBox.focus();
        }
    };

    xhr.send(formData);
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
        btn.innerHTML = "Dark mode"
    } else {
        localStorage.setItem('mode', 'dark');
        btn.innerHTML = "Light mode"
    }
}
// Apply dark/light mode from localStorage when the page loads
document.addEventListener("DOMContentLoaded", function() {
    var mode = localStorage.getItem('mode');
    if (mode === 'light') {
        document.body.classList.add('light-mode');
    }
});

// Actions
function handleAction(challenge) {
    changeUserText(challenge);
    submitForm();
}

function changeUserText(desiredText) {
    var textarea = document.querySelector('.user-msgbox');
    textarea.value = desiredText;
}