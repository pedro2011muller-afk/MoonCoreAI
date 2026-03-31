function openTab(tabName) {
    var i, tabcontent, tablinks;
    tabcontent = document.getElementsByClassName("tabcontent");
    for(i=0;i<tabcontent.length;i++){tabcontent[i].style.display="none";}
    tablinks = document.getElementsByClassName("tablink");
    for(i=0;i<tablinks.length;i++){tablinks[i].classList.remove("active");}
    document.getElementById(tabName).style.display="block";
    event.currentTarget.classList.add("active");
}

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

function sendDevMessage() {
    let input = document.getElementById("devMsgInput");
    let msg = input.value.trim();
    if(msg === "") return;

    let chatBox = document.getElementById("devChatBox");
    chatBox.innerHTML += '<div class="message-user">'+msg+'</div>';

    fetch("/dev/chat", {
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