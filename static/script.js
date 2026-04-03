// 🐾 Animal icon detector
function getAnimalIcon(text) {
    text = text.toLowerCase();

    if (text.includes("lion")) return "🦁";
    if (text.includes("tiger")) return "🐯";
    if (text.includes("elephant")) return "🐘";
    if (text.includes("snake") || text.includes("reptile")) return "🐍";
    if (text.includes("monkey")) return "🐒";

    return "🌿";
}

// 💬 Send message
function send() {
    let msgInput = document.getElementById("msg");
    let msg = msgInput.value;

    if (!msg.trim()) return;

    let chatBox = document.getElementById("chat-box");

    // ✅ User message
    chatBox.innerHTML += `
        <div class="user">
            <span>${msg}</span>
        </div>
    `;

    chatBox.scrollTop = chatBox.scrollHeight;

    // ⌛ Typing indicator
    let typing = document.createElement("div");
    typing.className = "bot typing";
    typing.innerHTML = "<span>Typing...</span>";
    chatBox.appendChild(typing);
    chatBox.scrollTop = chatBox.scrollHeight;

    fetch("/chat", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ message: msg })
    })
    .then(res => res.json())
    .then(data => {

        // ❌ Remove typing indicator
        typing.remove();

        let icon = getAnimalIcon(data.reply);

        // ✅ Bot response with image support
        chatBox.innerHTML += `
            <div class="bot">
                <span>${icon} ${data.reply}</span><br>
                ${data.image ? `<img src="${data.image}" width="150" style="border-radius:10px;margin-top:5px;">` : ""}
            </div>
        `;

        chatBox.scrollTop = chatBox.scrollHeight;
    })
    .catch(error => {
        typing.remove();

        chatBox.innerHTML += `
            <div class="bot">
                <span>⚠️ Error: Unable to connect</span>
            </div>
        `;

        chatBox.scrollTop = chatBox.scrollHeight;
    });

    // Clear input
    msgInput.value = "";
}

// ⌨️ Enter key support
document.getElementById("msg").addEventListener("keypress", function(e) {
    if (e.key === "Enter") {
        send();
    }
});

// 🎤 Voice input
function startVoice() {
    const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();

    recognition.lang = "en-IN";

    recognition.onresult = function(event) {
        let speech = event.results[0][0].transcript;
        document.getElementById("msg").value = speech;
        send();
    };

    recognition.start();
}

// 📍 Mock location-based suggestion
function getLocationAnimals(lat, lon) {
    if (lat > 12.8) return "You are near the Lion enclosure 🦁";
    else return "You are near the Reptile House 🐍";
}

// 📍 Where am I feature
function whereAmI() {
    let chatBox = document.getElementById("chat-box");

    navigator.geolocation.getCurrentPosition(position => {
        let msg = getLocationAnimals(
            position.coords.latitude,
            position.coords.longitude
        );

        chatBox.innerHTML += `
            <div class="bot">
                <span>📍 ${msg}</span>
            </div>
        `;

        chatBox.scrollTop = chatBox.scrollHeight;
    });
}