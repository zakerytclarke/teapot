import json
from search import Search

class ChatApp:
    def __init__(self,config_id):
        f = open (f'./configs/{config_id}.json', "r")
        self.config = json.loads(f.read())
        f.close()

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
                    self.search.addDocument(f"{image.get('caption')}",['image'],{'url':image.get('url'),'parent_url':page})

            # For document content
            for doc in page_json.get('documents'):
                self.search.addDocument(doc,['document'],{'parent_url':page})
        
        self.search.train()

    def handleChat(self, text):
        relevant_document = self.search.parse(text)
        print(relevant_document.content)
        import ipdb
        ipdb.set_trace()
        print(text)

chatbot = ChatApp("gaonurri")
chatbot.handleChat("Can I see your drinks menu?")