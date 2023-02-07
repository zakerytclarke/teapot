import requests
import json
from search import Search
from config import get_template
from create_customer import create_deployment
import sys
from pathlib import Path


def query_forefront(data):
    headers = {
    "Authorization": "Bearer 82940da568924bb08a0edb3b",
    "Content-Type": "application/json"
    }

    body = {
        "text": data,
        "top_p": 1,
        "top_k": 40,
        "temperature": 0.7,
        "repetition_penalty":  1,
        "length": 50,
        "stop_sequences": ["User:","Bot:"]
    }

    res = requests.post(
        "https://shared-api.forefront.link/organization/Rb6PHWZExYgI/gpt-j-6b-vanilla/completions/2JrDQ5BhJAm6",
        json=body,
        headers=headers
    )

    result = res.json()

    return result.get('result')[0].get('completion').strip()
    

class ChatApp:
    def __init__(self,config_id):
        f = open (f'./configs/{config_id}.json', "r")
        self.config = json.loads(f.read())
        f.close()
        self.template = get_template(self.config.get('template'))
        self.chats = [
            {'from':'Bot','message':self.template.get('intro')},
        ]

        # Generate Search 
        self.search = Search()
        # Add social tags
        for social in self.config.get('website').get('social'):
            url = self.config.get('website').get('social')[social]
            if len(url)>0:
                self.search.addDocument(f"Link for {social}: {url[0]}",['links'],{'url':url[0]})
        # Add page content
        for page in self.config.get('website').get('pages'):
            page_json = self.config.get('website').get('pages')[page]
            
            # For text content
            for content in page_json.get('content'):
                if len(content)>10:
                    self.search.addDocument(content,['content'],{'parent_url':page})
            
            # For Image content
            for image in page_json.get('images'):
                if image.get('alt'):
                    self.search.addDocument(f"{image.get('caption')+image.get('url')}",['image'],{'url':image.get('url'),'parent_url':page})

            # For document content
            for doc in page_json.get('documents'):
                self.search.addDocument(doc,['document'],{'parent_url':page})
        
        self.search.train()

    def getChatsText(self):
        return "\n".join(list(map(lambda x: f"{x.get('from')}: {x.get('message')}",self.chats)))


    def handleChat(self, text):
        relevant_documents = self.search.get_top_results(text,50)

        search_info = '\n'.join(list(map(lambda x:x.content, relevant_documents)))
        print(f"Info:{search_info}")
        import ipdb
        ipdb.set_trace()
        self.chats.append({'from':"User",'message':text})
        text_query = self.template.get('description') + "\n" + self.template.get('priming') + "\n\n" + self.template.get('context') + "\n" + self.getChatsText() + "Info:" + search_info +"\n"+ "Bot: "
        result = query_forefront(text_query)
        self.chats.append({'from':"Bot",'message':result})
        return result
        





def main():
    customer_name = sys.argv[1]
    path = Path(f'./configs/{customer_name}.json')

    if not path.is_file(): # Deployment doesn't exist
        print("Customer doesn't exist. Create Deployment?")
        customer_url = input("Url:")
        customer_type = input("Template:")
        create_deployment(customer_name,customer_url,customer_type)

    print(f"Loading {customer_name}")
    chatbot = ChatApp(customer_name)
    while True:
        print(f"Bot:{chatbot.handleChat(input('User:'))}")



if __name__ == "__main__":
    main()