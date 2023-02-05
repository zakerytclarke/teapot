from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
from sklearn.pipeline import Pipeline
import re
class Document:
    content=""
    tags=[]
    metadata=""
    def __init__(self,contents,tags=[],metadata={}):
        self.content = contents
        self.tags = tags
        self.metadata = metadata
class Search:
    def __init__(self):
        self.tokenizer = TfidfVectorizer(sublinear_tf=True, norm='l2', encoding='latin-1', ngram_range=(1, 2), stop_words='english')
        self.model = NearestNeighbors(n_neighbors=5)

        self.documents = []
        self.mapping = {}


    def addDocument(self,contents,tags=[],metadata={}):
        self.documents.append(Document(contents,tags,metadata))
    def train(self):
        
        self.tokenizer = self.tokenizer.fit(list(map(lambda x:re.sub('[^0-9a-zA-Z]+', ' ', x.content),self.documents)))
        tokens = self.tokenizer.transform(list(map(lambda x:x.content,self.documents)))
        self.model = self.model.fit(tokens)


    def parse(self,text):
        neighbors = self.model.kneighbors(self.tokenizer.transform([text]),1,return_distance=False)[0]
        return self.documents[neighbors[0]]
        
# search = Search()
# search.addDocument("Thomas Jefferson (April 13, 1743[a] - July 4, 1826) was an American statesman, diplomat, lawyer, architect, philosopher, slaver, and Founding Father who served as the third president of the United States from 1801 to 1809. He was previously the nation's second vice president under John Adams and the first United States secretary of state under George Washington. The principal author of the Declaration of Independence, Jefferson was a proponent of democracy, republicanism, and individual rights, motivating American colonists to break from the Kingdom of Great Britain and form a new nation. He produced formative documents and decisions at state, national, and international levels.")
# search.addDocument("George Washington (February 22, 1732[b] - December 14, 1799) was an American military officer, statesman, and Founding Father who served as the first president of the United States from 1789 to 1797. Appointed by the Continental Congress as commander of the Continental Army, Washington led Patriot forces to victory in the American Revolutionary War and served as president of the Constitutional Convention of 1787, which created and ratified the Constitution of the United States and the American federal government. Washington has been called the 'Father of his Country' for his manifold leadership in the nation's founding")
# search.addDocument("Our phone number is 505-234-9665")
# search.train()
# print(search.parse("Who was an architect?").content)
# print(search.parse("Who was first?").content)
# print(search.parse("Who was phone?").content)