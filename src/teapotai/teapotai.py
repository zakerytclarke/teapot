from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM, logging
import joblib
import torch
import numpy as np
from sklearn.neural_network import MLPClassifier
from sklearn.metrics.pairwise import cosine_similarity
from pydantic import BaseModel, Field, ValidationError
from pydantic.functional_validators import BeforeValidator
from pydantic_core.core_schema import no_info_plain_validator_function
from pydantic import field_validator
import inspect
from typing import List, Optional, Callable, get_origin, get_args, Type
from tqdm import tqdm
import re
import os
from langsmith import traceable
import joblib
import pkg_resources

logging.set_verbosity_error()

DEFAULT_MODEL = "teapotai/teapotllm"
DEFAULT_MODEL_REVISION = "699ab39cbf586674806354e92fbd6179f9a95f4a"
DEFAULT_SYSTEM_PROMPT = """You are Teapot, an open-source AI assistant optimized for low-end devices, providing short, accurate responses without hallucinating while excelling at information extraction and text summarization."""


class TeapotAISettings(BaseModel):
    """
    Settings configuration for TeapotAI.

    Attributes:
        use_rag (bool): Whether to use RAG (Retrieve and Generate).
        rag_num_results (int): Number of top documents to retrieve based on similarity.
        rag_similarity_threshold (float): Similarity threshold for document relevance.
        max_context_length (int): Maximum length of context to consider.
        context_chunking (bool): Whether to chunk context for processing.
        max_tool_calls (int): Maximum number of tool calls allowed.
        verbose (bool): Whether to print verbose updates.
        log_level (str): Log level setting (e.g., 'info', 'debug').
    """
    use_rag: bool = True
    rag_num_results: int = 3
    rag_similarity_threshold: float = 0.5
    max_context_length: int = 512
    context_chunking: bool = True
    allow_tool_use:bool = True
    max_tool_calls:int = 1
    verbose: bool = True
    log_level: str = "info"

class TeapotTool(BaseModel):
    name: str = Field(..., description="The name of the tool.")
    description: str = Field(..., description="A description of what the tool does.")
    schema: Type[BaseModel] = Field(..., description="A Pydantic model defining the tool's input schema.")
    fn: Callable = Field(..., description="The function that implements the tool logic.")
    directly_return_result: bool = False

    class Config:
        arbitrary_types_allowed = True

class TeapotAI:
    """
    TeapotAI class for generating responses based on queries and context, optionally using RAG.

    Attributes:
        model (str): The model name for TeapotAI.
        settings (TeapotAISettings): Settings configuration for TeapotAI.
        tokenizer (AutoTokenizer): The tokenizer for the model.
        generator (pipeline): The text-to-text generation pipeline.
        documents (List[str]): List of documents used for context retrieval.
        embedding_model (pipeline): Embedding model for document retrieval.
        document_embeddings (np.ndarray): Pre-generated embeddings for the documents.
    """

    def __init__(self, model = None, tokenizer = None, documents: List[str] = [], tools: List[TeapotTool] = [], settings: TeapotAISettings = TeapotAISettings()):
        """
        Initializes the TeapotAI class.

        Args:
            model (str): The model name for TeapotAI.
            documents (List[str]): List of documents to use for context retrieval.
            settings (TeapotAISettings): The settings configuration for TeapotAI.
        """
        self.settings = settings
        if self.settings.verbose:
            print(""" _____                      _         _    ___        __o__    _;;
|_   _|__  __ _ _ __   ___ | |_      / \  |_ _|   __ /-___-\__/ /
  | |/ _ \/ _` | '_ \ / _ \| __|    / _ \  | |   (  |       |__/
  | |  __/ (_| | |_) | (_) | |_    / ___ \ | |    \_|~~~~~~~|
  |_|\___|\__,_| .__/ \___/ \__/  /_/   \_\___|      \_____/
               |_|   """)

        if self.settings.verbose:
            print(f"Loading Model")

        if model is None:
            model = AutoModelForSeq2SeqLM.from_pretrained(
                DEFAULT_MODEL,
                revision=DEFAULT_MODEL_REVISION,
              )
        if tokenizer is None:
            tokenizer = AutoTokenizer.from_pretrained(
                DEFAULT_MODEL,
                revision=DEFAULT_MODEL_REVISION
            )

        self.model = model
        self.tokenizer = tokenizer

        # Get the path of the model file within the package
        model_path = pkg_resources.resource_filename('teapotai', 'teapot_refusal_classifier.joblib')

        
        self.refusal_detector = joblib.load(model_path)


        self.documents = [chunk for document in documents for chunk in self._chunk_document(document)]
        self.tools = tools
        
        if self.settings.use_rag:
            self.embedding_model = pipeline("feature-extraction", model="teapotai/teapotembedding", truncation=True)
            self.document_embeddings = self._generate_document_embeddings(self.documents)

    def _chunk_document(self, context: str) -> List[str]:
        """
        Chunk the input context into smaller segments if necessary based on the settings.

        Args:
            context (str): The document context to chunk.

        Returns:
            List[str]: A list of chunked document strings.
        """
        if self.settings.context_chunking:
            tokenized_context = self.tokenizer(context).get("input_ids")
            if len(tokenized_context) > self.tokenizer.model_max_length:
                paragraphs = context.split("\n\n")
                documents = []
                for paragraph in paragraphs:
                    tokens = self.tokenizer(paragraph).get("input_ids")
                    if len(tokens) > self.tokenizer.model_max_length:
                        for i in range(0, len(tokens), self.tokenizer.model_max_length):
                            chunk_tokens = tokens[i:i + self.tokenizer.model_max_length]
                            chunk_text = self.tokenizer.decode(chunk_tokens, skip_special_tokens=True)
                            documents.append(chunk_text)
                    else:
                        documents.append(paragraph)
                return documents
            else:
                return [context]
        else:
            return [context]

    def _generate_document_embeddings(self, documents: List[str]) -> np.ndarray:
        """
        Generate embeddings for the provided documents using the embedding model.

        Args:
            documents (List[str]): A list of document strings to generate embeddings for.

        Returns:
            np.ndarray: A NumPy array of document embeddings.
        """
        embeddings = []

        if self.settings.verbose:
            print("Generating embeddings for documents...")
            for doc in tqdm(documents, desc="Document Embedding", unit=" doc"):
                embeddings.append(self.embedding_model(doc)[0][0])
                # embeddings.append(np.mean(self.embedding_model(doc, truncation=True)[0], axis=0))
        else:
            for doc in documents:
                embeddings.append(self.embedding_model(doc)[0][0])
                # embeddings.append(np.mean(self.embedding_model(doc, truncation=True)[0], axis=0))

        return np.array(embeddings)

    def _retrieval(self, query: str, documents: List[str], document_embeddings: np.ndarray) -> List[str]:
        """
        Retrieve the most relevant documents based on cosine similarity to the query.

        Args:
            query (str): The query string for retrieval.
            documents (List[str]): List of document strings to search through.
            document_embeddings (np.ndarray): The embeddings for the documents.

        Returns:
            List[str]: A list of top relevant documents based on the query.
        """
        query_embedding = self.embedding_model(query)[0][0]
        # query_embedding = np.mean(self.embedding_model(query, truncation=True)[0], axis=0)
        similarities = cosine_similarity([query_embedding], document_embeddings)[0]
        filtered_indices = [i for i, similarity in enumerate(similarities) if similarity >= self.settings.rag_similarity_threshold]
        top_n_indices = sorted(filtered_indices, key=lambda i: similarities[i], reverse=True)[:self.settings.rag_num_results]

        return [documents[i] for i in top_n_indices]

    def rag(self, query: str) -> List[str]:
        """
        Perform Retrieval-Augmented Generation (RAG) based on the query and the documents.

        Args:
            query (str): The query string to perform RAG on.

        Returns:
            List[str]: A list of top documents retrieved using RAG.
        """
        if not self.settings.use_rag or not self.documents:
            return []

        return self._retrieval(query, self.documents, self.document_embeddings)

    def _detect_refusal(self, input_text:str) -> bool:
      # Teapotllm is consistent with refusal format
      if "I'm sorry" in input_text or "I don't" in input_text:
          return True
      # Invoke custom refusal detection model for more complicated queries
      embedding = np.mean(self.embedding_model(input_text, truncation=True)[0], axis=0)
      score = float(self.refusal_detector.predict_proba([embedding])[0][1])
      return score > 0.5


    @traceable
    def generate(self, input_text: str) -> str:
        """
        Generate text based on the input string using the TeapotLLM model.

        Args:
            input_text (str): The text prompt to generate a response for.

        Returns:
            str: The generated output from the model.
        """
        # Tokenize the input text
        inputs = self.tokenizer(input_text, return_tensors="pt")

        # Generate output (model inference)
        outputs = self.model.generate(**inputs, max_length=512)

        # Decode the generated output
        result = self.tokenizer.decode(outputs[0], skip_special_tokens=True)


        if self.settings.log_level == "debug":
            print("="*100)
            print(input_text)
            print(result)

        return result

    @traceable
    def query(self, query: str, context: str = "", system_prompt: str = DEFAULT_SYSTEM_PROMPT, recursive_depth: int = None) -> str:
        """
        Handle a query and context, using RAG if no context is provided, and return a generated response.

        Args:
            query (str): The query string to be answered.
            context (str): The context to guide the response. Defaults to an empty string.

        Returns:
            str: The generated response based on the input query and context.
        """


        if self.settings.use_rag:
            rag_context = "\n\n".join(self.rag(query))

        full_context = f"{rag_context}\n{context}"

        if self.settings.context_chunking:
            documents = self._chunk_document(context)
            if len(documents) > self.settings.rag_num_results:
                document_embeddings = self._generate_document_embeddings(documents)
                rag_documents = self._retrieval(query, documents, document_embeddings)
                full_context = rag_context + "\n\n" + "\n\n".join(rag_documents)

        input_text = f"{full_context}\n{system_prompt}\n{query}"

        result = self.generate(input_text)

        if self.settings.allow_tool_use and len(self.tools) > 0: # Tool use enabled
            if recursive_depth is None:
                recursive_depth = self.settings.max_tool_calls
            # Check if we have hit recusrve depth
            if recursive_depth > 0:
              if self._detect_refusal(result):
                  selected_tool_name = self.generate(f"{chr(10).join(f'{t.name} - {t.description}' for t in self.tools)}\nQuery: '{query}'\nExtract the name of the tool to use:")
                  selected_tool = [tool for tool in self.tools if tool.name.lower()==selected_tool_name.lower()]
                  if len(selected_tool) > 0:
                    try: # Attempt to extract tool schema and use
                      tool_extraction = self.extract(selected_tool[0].schema, query=f"Query:'{query}' (If you can't extract return None)")
                      tool_result = selected_tool[0].fn(tool_extraction)
                    except ValidationError as e:
                      tool_result = f"Error: Unable to use tool"
                    if selected_tool[0].directly_return_result:
                      result = tool_result
                    else:
                      result = self.query(query=input_text, context=f"{selected_tool[0].name}({tool_extraction}) => {tool_result}", system_prompt=system_prompt, recursive_depth = recursive_depth - 1)

        return result

    @traceable
    def chat(self, conversation_history: List[dict]) -> str:
        """
        Engage in a chat by taking a list of previous messages and generating a response.

        Args:
            conversation_history (List[dict]): A list of previous messages, each containing 'content'.

        Returns:
            str: The generated response based on the conversation history.
        """
        last_user_index = next(
            (i for i in reversed(range(len(conversation_history))) if conversation_history[i].get('role') == 'user'),
            None
        )

        if last_user_index is not None:
            last_user_message = conversation_history[last_user_index]
            history_without_last_user = conversation_history[:last_user_index] + conversation_history[last_user_index + 1:]

            chat_history = "".join([
                f"{msg.get('role', '')}: {msg.get('content', '')}\n"
                for msg in history_without_last_user
            ])
            formatted_last_user = f"user: {last_user_message.get('content', '')}"
        else:
            chat_history = ""
            formatted_last_user = ""

        return self.query(query=formatted_last_user, context=chat_history)

    @traceable
    def extract(self, class_annotation: BaseModel, query: str = "", context: str = "") -> BaseModel:
        """
        Extract fields from a Pydantic class annotation by querying and processing each field.

        Args:
            class_annotation (BaseModel): The Pydantic class to extract fields from.
            query (str): The query string to guide the extraction. Defaults to an empty string.
            context (str): Optional context for the query.

        Returns:
            BaseModel: An instance of the provided Pydantic class with extracted field values.
        """
        if self.settings.use_rag and context is not None:
            context_documents = self.rag(query)
            context = "\n".join(context_documents) + context

        output = {}
        for field_name, field in class_annotation.model_fields.items():
            type_annotation = field.annotation
            description = field.description
            description_annotation = f"({description})" if description else ""

            result = self.generate(f"{query}\nExtract the field {field_name} {description_annotation}")

            if type_annotation == bool or type_annotation == Optional[bool]:
                parsed_result = (
                    True if re.search(r'\b(yes|true)\b', result, re.IGNORECASE)
                    else (False if re.search(r'\b(no|false)\b', result, re.IGNORECASE) else None)
                )
            elif type_annotation in [int, float, Optional[int], Optional[float]]:
                cleaned = re.sub(r'[^0-9.-]', '', result)  # Allow negative and decimal
                if cleaned:
                    try:
                        parsed_result = type_annotation(cleaned)
                    except Exception:
                        parsed_result = None
                else:
                    parsed_result = None
            elif type_annotation == str or type_annotation == Optional[str]:
                if result is not None:
                  parsed_result = result.strip()
                else:
                  parsed_result = result
            else:
                raise ValueError(f"Teapot- Unsupported type annotation: {type_annotation}")


            output[field_name] = parsed_result

        return class_annotation(**output)