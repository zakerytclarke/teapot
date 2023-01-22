var teapot_wrapper = document.createElement("div");
teapot_wrapper.id="teapot-chat-wrapper";
teapot_wrapper.innerHTML=`
<style>
#teapot-chat-wrapper{
    width:80%;
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

var CONFIG = {
    client_id:'realtor'
}

var SESSION = {};


onload();

async function onload(){
    SESSION = {
        'chats':[
            {'bot':'Hi, I am Teapot AI, how can I help you?'},
        ]
    }
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
    SESSION.chats.push({
        'user':message
    })

}
