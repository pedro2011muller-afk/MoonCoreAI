function sendMessage() {
    let input = document.getElementById("msgInput");
    let msg = input.value.trim();
    if(msg === "") return;

    let chatBox = document.getElementById("chatBox");

    // mensagem do usuário
    let userDiv = document.createElement("div");
    userDiv.className = "message-user";
    userDiv.innerHTML = msg;
    chatBox.appendChild(userDiv);

    // mensagem da IA com leve delay
    let aiDiv = document.createElement("div");
    aiDiv.className = "message-ai";
    aiDiv.innerHTML = "Digitando...";
    chatBox.appendChild(aiDiv);

    chatBox.scrollTop = chatBox.scrollHeight;

    fetch("/chat", {
        method: "POST",
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({message: msg})
    })
    .then(res => res.json())
    .then(data => {
        setTimeout(() => {
            aiDiv.innerHTML = data.response;
            chatBox.scrollTop = chatBox.scrollHeight;
        }, 200); // delay leve de 200ms para parecer natural
    });

    input.value = "";
}

// Enter pula linha, Shift+Enter envia
document.getElementById("msgInput").addEventListener("keydown", function(e){
    if(e.key === "Enter" && !e.shiftKey){
        e.preventDefault();
        sendMessage();
    }
});