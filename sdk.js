var teapot_wrapper = document.createElement("div");
teapot_wrapper.id="teapot-chat-wrapper";
teapot_wrapper.innerHTML=`
<style>
#teapot-chat-wrapper{
    width:80%;
    min-height:400px;
    border-radius:2vw;
    background-color:#d2d4da;
    text-align:center;
    text-shadow:none;
    min-width:600px;
}
#teapot-chat-wrapper input{
    border-radius:1vw;
    width:80%;
    border:#ccc 1px;
    font-size: 100%;
    padding:3px;
    padding-left:10px;
    padding-right:10px;

}

#teapot-chat-header{
    color:#2d3d3e;
    font-size:200%;
    text-align:center;
    background-color:#f2f8fd; 
    overflow:hidden;
    border-radius:0.5vw;  
}

#teapot-chat-messages{
 background-color:#f2f2f2;   
 
 border-radius:0.5vw;  
 
 padding:20px;
}

.message{
    width:50%;
    color:#fefefe;
    border-radius:2vw;
    padding:5px;
    padding-left:10px;
    padding-right:10px;
}
.messageUser{
    background-color:#43CC47;
    margin-left:45%
}
.messageBot{
    background-color:#1982FC;
}
</style>

<div id="teapot-chat-header">
    Realtor AI
</div>
<div id="teapot-chat-messages">
</div>
<input id="teapot-chat-box" type="text"><button onclick="sendMessage()">Send</button>
`;
document.getElementById("teapot").after(teapot_wrapper);

var teapot;


onload();

async function onload(){
    teapot = new Teapot('chatter');
    renderMessages()
}

function renderMessages(){
    document.getElementById("teapot-chat-messages").innerHTML = "";
    for(var i=0;i<teapot.chats.length;i++){
        if(teapot.chats[i].from=="User"){
            document.getElementById("teapot-chat-messages").innerHTML += `
                <p class="message messageUser">${teapot.chats[i].message}</p>
            `;
        }

        if(teapot.chats[i].from=="Bot"){
            document.getElementById("teapot-chat-messages").innerHTML += `
                <p class="message messageBot">${teapot.chats[i].message}</p>
            `;
        }

    }
}

async function sendMessage(){
    var message = document.getElementById("teapot-chat-box").value;
    document.getElementById("teapot-chat-box").value="";
    await teapot.handleChat(message);
    renderMessages();
}
