from transformers import pipeline
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from pydantic import BaseModel
from typing import List, Optional
from tqdm import tqdm
import re


class TeapotAISettings(BaseModel):
    """
    Pydantic settings model for TeapotAI configuration.
    
    Attributes:
        use_rag (bool): Whether to use RAG (Retrieve and Generate).
        rag_num_results (int): Number of top documents to retrieve based on similarity.
        rag_similarity_threshold (float): Similarity threshold for document relevance.
        verbose (bool): Whether to print verbose updates.
        log_level (str): The log level for the application (e.g., "info", "debug").
    """
    use_rag: bool = True  # Whether to use RAG (Retrieve and Generate)
    rag_num_results: int = 3  # Number of top documents to retrieve based on similarity
    rag_similarity_threshold: float = 0.5  # Similarity threshold for document relevance
    verbose: bool = True  # Whether to print verbose updates
    log_level: str = "info"  # Log level setting (e.g., 'info', 'debug')


class TeapotAI:
    """
    TeapotAI class that interacts with a language model for text generation and retrieval tasks.
    
    Attributes:
        model (str): The model identifier.
        model_revision (Optional[str]): The revision/version of the model.
        api_key (Optional[str]): API key for accessing the model (if required).
        settings (TeapotAISettings): Configuration settings for the AI instance.
        generator (callable): The pipeline for text generation.
        embedding_model (callable): The pipeline for feature extraction (document embeddings).
        documents (List[str]): List of documents for retrieval.
        document_embeddings (np.ndarray): Embeddings for the provided documents.
    """
    
    def __init__(self, model_revision: Optional[str] = None, api_key: Optional[str] = None,
                 documents: List[str] = [], settings: TeapotAISettings = TeapotAISettings()):
        """
        Initializes the TeapotAI class with optional model_revision and api_key.

        Parameters:
            model_revision (Optional[str]): The revision/version of the model to use.
            api_key (Optional[str]): The API key for accessing the model if needed.
            documents (List[str]): A list of documents for retrieval. Defaults to an empty list.
            settings (TeapotAISettings): The settings configuration (defaults to TeapotAISettings()).
        """
        self.model = "teapotai/teapotllm"
        self.model_revision = model_revision
        self.api_key = api_key
        self.settings = settings
        
        if self.settings.verbose:
            print(""" _____                      _         _    ___        __o__    _;; 
|_   _|__  __ _ _ __   ___ | |_      / \  |_ _|   __ /-___-\__/ /
  | |/ _ \/ _` | '_ \ / _ \| __|    / _ \  | |   (  |       |__/
  | |  __/ (_| | |_) | (_) | |_    / ___ \ | |    \_|~~~~~~~|
  |_|\___|\__,_| .__/ \___/ \__/  /_/   \_\___|      \_____/
               |_|   """)
        
        if self.settings.verbose:
            print(f"Loading Model: {self.model} Revision: {self.model_revision or 'Latest'}")
        
        self.generator = pipeline("text2text-generation", model=self.model, revision=self.model_revision) if model_revision else pipeline("text2text-generation", model=self.model)
        
        self.documents = documents
        
        if self.settings.use_rag and self.documents:
            self.embedding_model = pipeline("feature-extraction", model="teapotai/teapotembedding")
            self.document_embeddings = self._generate_document_embeddings(self.documents)

    def _generate_document_embeddings(self, documents: List[str]) -> np.ndarray:
        """
        Generate embeddings for the provided documents using the embedding model.

        Parameters:
            documents (List[str]): A list of document strings to generate embeddings for.

        Returns:
            np.ndarray: A NumPy array of document embeddings.
        """
        embeddings = []
        
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
        Perform RAG (Retrieve and Generate) by finding the most relevant documents based on cosine similarity.

        Parameters:
            query (str): The query string to find relevant documents for.

        Returns:
            List[str]: A list of the top N most relevant documents.
        """
        if not self.settings.use_rag or not self.documents:
            return []

        query_embedding = self.embedding_model(query)[0][0]
        similarities = cosine_similarity([query_embedding], self.document_embeddings)[0]

        filtered_indices = [i for i, similarity in enumerate(similarities) if similarity >= self.settings.rag_similarity_threshold]
        top_n_indices = sorted(filtered_indices, key=lambda i: similarities[i], reverse=True)[:self.settings.rag_num_results]

        return [self.documents[i] for i in top_n_indices]

    def generate(self, input_text: str) -> str:
        """
        Generate text based on the input string using the teapotllm model.

        Parameters:
            input_text (str): The text prompt to generate a response for.

        Returns:
            str: The generated output from the model.
        """
        generated_text = self.generator(input_text)
        result = generated_text[0]['generated_text']
        
        if self.settings.log_level == "debug":
            print(input_text)
            print(result)
        
        return result

    def query(self, query: str, context: str = "") -> str:
        """
        Handle a query and context, using RAG if no context is provided, and return a generated response.

        Parameters:
            query (str): The query string to be answered.
            context (str): The context to guide the response. Defaults to an empty string.

        Returns:
            str: The generated response based on the input query and context.
        """
        if self.settings.use_rag and not context:
            context = "\n".join(self.rag(query))  # Perform RAG if no context is provided
        
        input_text = f"Context: {context}\nQuery: {query}"
        return self.generate(input_text)

    def chat(self, conversation_history: List[dict]) -> str:
        """
        Engage in a chat by taking a list of previous messages and generating a response.

        Parameters:
            conversation_history (List[dict]): A list of previous messages, each containing 'content'.

        Returns:
            str: The generated response based on the conversation history.
        """
        chat_history = "".join([message['content'] + "\n" for message in conversation_history])

        if self.settings.use_rag:
            context_documents = self.rag(chat_history)  # Perform RAG on the conversation history
            context = "\n".join(context_documents)
            chat_history = f"Context: {context}\n" + chat_history

        return self.generate(chat_history + "\n" + "agent:")

    def extract(self, class_annotation: BaseModel, query: str = "", context: str = "") -> BaseModel:
        """
        Extract fields from a Pydantic class annotation by querying and processing each field.

        Parameters:
            class_annotation (BaseModel): The Pydantic class to extract fields from.
            query (str): The query string to guide the extraction. Defaults to an empty string.
            context (str): Optional context for the query.

        Returns:
            BaseModel: An instance of the provided Pydantic class with extracted field values.
        """
        if self.settings.use_rag:
            context_documents = self.rag(query)
            context = "\n".join(context_documents) + context
        
        output = {}
        for field_name, field in class_annotation.__fields__.items():
            type_annotation = field.annotation
            description = field.description
            description_annotation = f"({description})" if description else ""

            result = self.query(f"Extract the field {field_name} {description_annotation} to a {type_annotation}", context=context)

            # Process result based on field type
            if type_annotation == bool:
                parsed_result = (
                    True if re.search(r'\b(yes|true)\b', result, re.IGNORECASE)
                    else (False if re.search(r'\b(no|false)\b', result, re.IGNORECASE) else None)
                )
            elif type_annotation in [int, float]:
                parsed_result = re.sub(r'[^0-9.]', '', result)
                if parsed_result:
                    try:
                        parsed_result = type_annotation(parsed_result)
                    except Exception:
                        parsed_result = None
                else:
                    parsed_result = None
            elif type_annotation == str:
                parsed_result = result.strip()
            else:
                raise ValueError(f"Unsupported type annotation: {type_annotation}")

            output[field_name] = parsed_result
        
        return class_annotation(**output)
