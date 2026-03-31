function sendMessage() {
    let input = document.getElementById("msgInput");
    let msg = input.value.trim();
    if(msg === "") return;

    let chatBox = document.getElementById("chatBox");
    chatBox.innerHTML += '<div class="message-user">'+msg+'</div>';

    fetch("/chat", {
        method: "POST",
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({message: msg})
    })
    .then(res => res.json())
    .then(data => {
        chatBox.innerHTML += '<div class="message-ai">'+data.response+'</div>';
        chatBox.scrollTop = chatBox.scrollHeight;
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