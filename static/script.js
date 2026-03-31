function sendMessage() {
    let input = document.getElementById("msgInput");
    let msg = input.value.trim();
    if(msg === "") return;

    let chatBox = document.getElementById("chatBox");
    chatBox.innerHTML += '<div class="message-user">'+msg+'</div>';

    // Simular digitação da IA
    chatBox.innerHTML += '<div class="message-ai" id="aiTyping">Digitando...</div>';
    chatBox.scrollTop = chatBox.scrollHeight;

    fetch("/chat", {
        method: "POST",
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({message: msg})
    })
    .then(res => res.json())
    .then(data => {
        let aiDiv = document.getElementById("aiTyping");
        aiDiv.innerHTML = '';
        let resposta = data.response;
        // efeito de digitação
        let i = 0;
        function digitar() {
            if(i < resposta.length){
                aiDiv.innerHTML += resposta.charAt(i);
                i++;
                setTimeout(digitar, 25);
            }
        }
        digitar();
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