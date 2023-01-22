document.getElementById("teapot").innerHTML +=`
<div id="teapot-chat-wrapper">
    <div id="teapot-chat-header">
        Realtor AI
    </div>
    <div id="teapot-chat-messages">
    </div>
    <input id="teapot-chat-box" type="text"><button onclick="sendMessage()">Send</button>
</div>
`;

var CONFIG = {
    client_id:'realtor'
}

var SESSION = {};


onload();

async function onload(){
    fetch(`api/create?client_id=${CONFIG.client_id}`).then((response) => response.json()).then(function(response){
        SESSION=response;
        renderMessages();
    });
}

function renderMessages(){
    document.getElementById("teapot-chat-messages").innerHTML = "";
    for(var i=0;i<SESSION.chats.length;i++){
        if(SESSION.chats[i].user){
            document.getElementById("teapot-chat-messages").innerHTML += `
                <p class="message messageUser">${SESSION.chats[i].user}</p>
            `;
        }
        if(SESSION.chats[i].bot){
            document.getElementById("teapot-chat-messages").innerHTML += `
                <p class="message messageBot">${SESSION.chats[i].bot}</p>
            `;
        }

    }
}

function sendMessage(){
    var message = document.getElementById("teapot-chat-box").value;
    document.getElementById("teapot-chat-box").value="";
    fetch(`api/interact?session_id=${SESSION.id}&message=${message}`).then((response) => response.json()).then(function(response){
        SESSION=response;
        renderMessages();
    });

}
