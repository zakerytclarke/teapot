// async function query(data) {
// 	const response = await fetch(
// 		"https://api-inference.huggingface.co/models/EleutherAI/gpt-j-6B",
// 		{
// 			headers: { Authorization: "Bearer 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" },
// 			method: "POST",
// 			body: JSON.stringify({inputs:data}),
// 		}
// 	);
// 	const result = await response.json();
// 	return result[0].generated_text;
// }

async function query(data) {
	const response = await fetch("https://model-api-shdxwd54ta-nw.a.run.app/generate/gptj", {
        "headers": {
          "accept": "*/*",
          "accept-language": "en-US,en;q=0.9",
          "content-type": "application/json",
          "developer_key": "sLdHjVjwMKd_7pd4C4l8S8yugfqq8caILaez7KJAmtKrZErnAOIVx_RoyOF6xRcAMvQ_yqlkxEWi87X0FIoaOg",
          "developer_uid": "mUCsg14rQqYbpRkcqMbiPKa29xg1",
          "sec-ch-ua": "\"Not_A Brand\";v=\"99\", \"Google Chrome\";v=\"109\", \"Chromium\";v=\"109\"",
          "sec-ch-ua-mobile": "?1",
          "sec-ch-ua-platform": "\"Android\"",
          "sec-fetch-dest": "empty",
          "sec-fetch-mode": "cors",
          "sec-fetch-site": "cross-site"
        },
        "referrer": "https://chai.ml/",
        "referrerPolicy": "strict-origin-when-cross-origin",
        "body": JSON.stringify({
            repetition_penalty: 1.1,
            response_length: 64,
            temperature: 0.6,
            text:data,
            top_k: 40,
            top_p: 1
        }),
        "method": "POST",
        "mode": "cors",
        "credentials": "omit"
      });
	const result = await response.json();
	return result.data;
}


class Teapot {
    constructor(config_key) {
        this.config = get_template(config_key);
        this.chats = [
            {'from':'Bot','message':this.config.intro},
        ];
    }
    
    getChatsText(){
        return this.chats.map(function(x){
            return `${x.from}: ${x.message}\n\n`
        })
        
    }

    async handleChat(message){
        this.chats.push({
            from:'User',
            message:message
        })
        var result = await query(this.config.description + "\n" + this.config.priming + "===\n\n" + this.config.context + "\n" + this.getChatsText() + "Bot: ")
        this.chats.push({
            from:'Bot',
            message:result
        })
    }
}


