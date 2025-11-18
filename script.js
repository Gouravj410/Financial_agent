const input = document.getElementById("user-input");
const sendBtn = document.getElementById("send-btn");
const chatBox = document.getElementById("chat-box");

// Add messages
function addMessage(sender, text, loading = false) {
  const msg = document.createElement("p");
  msg.classList.add(sender.toLowerCase());

  if (loading) {
    msg.innerHTML = `<strong>${sender}:</strong> <span class="loading">...</span>`;
  } else {
    msg.innerHTML = `<strong>${sender}:</strong> ${text}`;
  }

  chatBox.appendChild(msg);
  chatBox.scrollTop = chatBox.scrollHeight;
  return msg;
}

// Send message
async function sendMessage() {
  const question = input.value.trim();
  if (!question) return;

  addMessage("You", question);
  input.value = "";

  const loadingMsg = addMessage("Agent", "", true);

  try {
    const response = await fetch("http://127.0.0.1:8000/ask", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question }),
    });

    const data = await response.json();
    loadingMsg.innerHTML = `<strong>Agent:</strong> ${data.answer || "No response"}`;
  } catch (err) {
    loadingMsg.innerHTML = `<strong>Agent:</strong>Error connecting to server.`;
  }
}

sendBtn.addEventListener("click", sendMessage);
input.addEventListener("keypress", function (e) {
  if (e.key === "Enter") {
    sendMessage();
  }
});

