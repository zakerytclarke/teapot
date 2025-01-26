from transformers import pipeline

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from pydantic import BaseModel
from typing import List
from tqdm import tqdm
import re

# Pydantic Settings Model with verbose mode
class TeapotAISettings(BaseModel):
    use_rag: bool = True  # Whether to use RAG (Retrieve and Generate)
    rag_num_results: int = 3  # Number of top documents to retrieve based on similarity
    rag_similarity_threshold: float = 0.5  # Similarity threshold for document relevance
    verbose: bool = True  # Whether to print verbose updates

class TeapotAI:
    def __init__(self, model_revision=None, api_key=None, documents: List[str] = [], settings: TeapotAISettings = TeapotAISettings()):
        """
        Initializes the TeapotAI class with optional model_revision and api_key.

        Parameters:
        - model_revision (str, optional): The revision/version of the model to use.
        - api_key (str, optional): The API key for accessing the model if needed.
        - documents (list of str, optional): A list of documents for retrieval. Defaults to empty list.
        - settings (TeapotAISettings, optional): The settings configuration (defaults to TeapotAISettings()).
        """
        self.model="teapotai/teapotllm"
        self.model_revision = model_revision
        self.api_key = api_key
        self.settings = settings  # Store settings
        if self.settings.verbose:
          print(""" _____                      _         _    ___        __o__    _;; 
|_   _|__  __ _ _ __   ___ | |_      / \  |_ _|   __ /-___-\__/ /
  | |/ _ \/ _` | '_ \ / _ \| __|    / _ \  | |   (  |       |__/
  | |  __/ (_| | |_) | (_) | |_    / ___ \ | |    \_|~~~~~~~|
  |_|\___|\__,_| .__/ \___/ \__/  /_/   \_\___|      \_____/
               |_|   """)
        

        if self.settings.verbose:
          print(f"Loading Model: {self.model} Revision: {self.model_revision or 'Latest'}")
        # Initialize the text generation model (TeapotLLM)
        if model_revision:
            self.generator = pipeline("text2text-generation",  model=self.model, revision=model_revision)
        else:
            self.generator = pipeline("text2text-generation", model=self.model)
        
        # Initialize documents and embeddings (only if RAG is enabled and documents are passed)
        self.documents = documents

        if self.settings.use_rag and self.documents:
            self.embedding_model = pipeline("feature-extraction", model="teapotai/teapotembedding")
            self.document_embeddings = self._generate_document_embeddings(self.documents)

    def _generate_document_embeddings(self, documents: List[str]) -> np.ndarray:
        """
        Generate embeddings for the provided documents with verbose updates and tqdm progress bar.

        Parameters:
        - documents (list of str): A list of document strings to generate embeddings for.

        Returns:
        - np.ndarray: An array of document embeddings.
        """
        embeddings = []
        
        # Show progress bar if verbose is enabled
        if self.settings.verbose:
            print("Generating embeddings for documents...")
            for doc in tqdm(documents, desc="Document Embedding", unit="doc"):
                embeddings.append(self.embedding_model(doc)[0][0])
        else:
            for doc in documents:
                embeddings.append(self.embedding_model(doc)[0][0])
                
        return np.array(embeddings)

    def rag(self, query: str) -> List[str]:
        """
        Perform RAG (Retrieve and Generate) when no context is passed, by finding the most relevant
        documents using cosine similarity and returning the top n documents as a list of strings.

        Parameters:
        - query (str): The query string to find relevant documents for.

        Returns:
        - List[str]: A list of the top N most relevant documents.
        """
        if not self.settings.use_rag:
            return []

        # Generate the embedding for the query
        query_embedding = self.embedding_model(query)[0][0]
        
        # Compute cosine similarity between the query embedding and all document embeddings
        similarities = cosine_similarity([query_embedding], self.document_embeddings)[0]

        # Filter documents based on similarity threshold
        filtered_indices = [i for i, similarity in enumerate(similarities) if similarity >= self.settings.rag_similarity_threshold]

        # Select the top N documents or the filtered ones
        top_n_indices = sorted(filtered_indices, key=lambda i: similarities[i], reverse=True)[:self.settings.rag_num_results]

        # Select the top documents based on the indices
        top_documents = [self.documents[i] for i in top_n_indices]

        # Return the top documents as a list
        return top_documents

    def generate(self, input_text: str) -> str:
        """
        Generates text based on the input string using the teapotllm model.

        Parameters:
        - input_text (str): The text prompt to generate a response for.

        Returns:
        - str: The generated output from the model.
        """
        generated_text = self.generator(input_text)
        return generated_text[0]['generated_text']

    def query(self, query: str, context: str="") -> str:
        if self.settings.use_rag and not context:
            context = self.rag(query)  # Perform RAG if no context is provided
            
        input_text = f"Context: {context}\nQuery: {query}"
        return self.generate(input_text)

    def chat(self, conversation_history: List[dict]) -> str:
        
        chat_history = ""
        for message in conversation_history:
            chat_history += f"{message['content']}\n"
        
        if self.settings.use_rag:
            context_documents = self.rag(chat_history)  # Perform RAG on the conversation history
            context = "\n".join(context_documents)  # Concatenate the documents with newlines

            chat_history = f"Context: {context}\n" + chat_history

        return self.generate(chat_history+"\n"+"agent:")

    def extract(self, class_annotation, query: str="", context: str=""):
            
        if self.settings.use_rag:
            context_documents = self.rag(query)
            context = "\n".join(context_documents)  # Concatenate the documents with newlines
            
        output = {}
        for field_name, field in class_annotation.__fields__.items():
            type_annotation = field.annotation
            description = field.description
            description_annotation = f"({description})" if description else ""

            # Simulate query with teapot_ai
            result = self.query(f"Extract the field {field_name} {description_annotation} to a {type_annotation}", context=context)

            if type_annotation == bool:
                # Check if the result contains 'yes' or 'true' for True, or 'no' or 'false' for False
                parsed_result = (
                    True if re.search(r'\b(yes|true)\b', result, re.IGNORECASE)
                    else (False if re.search(r'\b(no|false)\b', result, re.IGNORECASE) else None)
                )
            elif type_annotation in [int, float]:
                # Extract numeric value
                parsed_result = re.sub(r'[^0-9.]', '', result)
                if parsed_result:
                    parsed_result = type_annotation(parsed_result)  # Convert to the correct type (int or float)
                else:
                    parsed_result = None  # Handle case where no valid number was found
            elif type_annotation == str:
                parsed_result = result.strip()  # Strip extra spaces or newlines
            else:
              assert False, f"Could not process the field '{field_name}' with type {type_annotation}"

            output[field_name] = parsed_result
        
        return class_annotation(**output)
