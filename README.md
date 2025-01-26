# TeapotAI Library

TeapotAI is a lightweight language model (~300 million parameters) optimized to run locally on resource-constrained devices such as smartphones and CPUs that can perform a variety of tasks, including hallucination resistance Question Answering, Retrieval Augmented Generation and JSON extraction.

## Learn More
Join our Discord [Link](https://discord.gg/hPxGSn5dST)
View our models [Link](https://huggingface.co/teapotai)


## Library
This library provides a wrapper around the base model to enable easier integrations into production environments.

## Installation

```bash
! pip install teapotai
```

---

## Use Cases

Here are three key use cases demonstrating how to use TeapotAI for different tasks:

---

### 1. General Question Answering (QA)

Teapot can be used for general question answering based on a passed in context. The model has been optimized to respond conversationally and is trained to not answer questions that can't be answered with a given context to avoid hallucinations.

#### Example:

```python
from teapotai import TeapotAI

# Sample context
context = """
The Eiffel Tower is a wrought iron lattice tower in Paris, France. It was designed by Gustave Eiffel and completed in 1889.
It stands at a height of 330 meters and is one of the most recognizable structures in the world.
"""

teapot_ai = TeapotAI()

answer = teapot_ai.query(query="What is the height of the Eiffel Tower?", context=context)
print(answer) # => "The Eiffel Tower stands at a height of 330 meters. "
```

#### Hallucination Example:

```python
from teapotai import TeapotAI

# Sample context without height information
context = """
The Eiffel Tower is a wrought iron lattice tower in Paris, France. It was designed by Gustave Eiffel and completed in 1889.
"""

teapot_ai = TeapotAI()

answer = teapot_ai.query(query="What is the height of the Eiffel Tower?", context=context)
print(answer) # => "I don't have information on the height of the Eiffel Tower."
```

---

### 2. Chat with Retrieval Augmented Generation (RAG)

TeapotAI can also use Retrieval Augmented Generation to determine which documents are relevant before answering a question. This is useful when you have multiple documents you want to use as context and want to ensure the model answers based on the most relevant ones.

#### Example:

```python
from teapotai import TeapotAI
# Sample documents (in practice, these could be articles or longer documents)
documents = [
    "The Eiffel Tower is located in Paris, France. It was built in 1889 and stands 330 meters tall.",
    "The Great Wall of China is a historic fortification that stretches over 13,000 miles.",
    "The Amazon Rainforest is the largest tropical rainforest in the world, covering over 5.5 million square kilometers.",
    "The Grand Canyon is a natural landmark located in Arizona, USA, carved by the Colorado River.",
    "Mount Everest is the tallest mountain on Earth, located in the Himalayas along the border between Nepal and China.",
    "The Colosseum in Rome, Italy, is an ancient amphitheater known for its gladiator battles.",
    "The Sahara Desert is the largest hot desert in the world, located in North Africa.",
    "The Nile River is the longest river in the world, flowing through northeastern Africa.",
    "The Empire State Building is an iconic skyscraper in New York City that was completed in 1931 and stands at 1454 feet tall."
]


# Initialize TeapotAI with documents for RAG
teapot_ai = TeapotAI(documents=documents)

# Get the answer using RAG
answer = teapot_ai.chat([
    {
        "role":"system",
        "content": "You are an agent designed to answer facts about famous landmarks."
    },
    {
        "role":"user",
        "content": "What landmark was constructed in the 1800s?"
    }
])
print(answer) # => The Eiffel Tower was constructed in the 1800s.
```

#### Loading RAG Model:
You may want to save a copy of a model with documents to reduce loading times by leveraging the pre-computed embeddings. TeapotAI is pickle compatible and can be saved/loaded as shown below.
```python
import pickle

# Pickle the TeapotAI model to a file with pre-computed embeddings
with open("teapot_ai.pkl", "wb") as f:
    pickle.dump(teapot_ai, f)


# Load the pickled model
with open("teapot_ai.pkl", "rb") as f:
    loaded_teapot_ai = pickle.load(f)

# You can now use the loaded instance as you would normally
print(len(loaded_teapot_ai.documents)) # => 10 Documents with precomputed embeddings

loaded_teapot_ai.query("What city is the Eiffel Tower in?") # => "The Eiffel Tower is located in Paris, France."

```

---

### Information Extraction

TeapotAI can be used to extract structured information from context using pre-defined json structures. The extract method takes a pydantic model that can be used to ensure Teapot extracts correct types. Teapot can infer fields based on names but also will leverage descriptions if available. This method can also be used with the RAG and query functioanlities natively.

#### Example:

```python
from teapotai import TeapotAI
from pydantic import BaseModel

# Sample text containing apartment details
apartment_description = """
This spacious 2-bedroom apartment is available for rent in downtown New York. The monthly rent is $2500.
It includes 1 bathrooms and a fully equipped kitchen with modern appliances.

Pets are welcome!

Please reach out to us at 555-123-4567 or john@realty.com
"""

# Define a Pydantic model for the data you want to extract
class ApartmentInfo(BaseModel):
    rent: float = Field(..., description="the monthly rent in dollars")
    bedrooms: int = Field(..., description="the number of bedrooms")
    bathrooms: int = Field(..., description="the number of bathrooms")
    phone_number: str

# Initialize TeapotAI
teapot_ai = TeapotAI()

# Extract the apartment details
extracted_info = teapot_ai.extract(ApartmentInfo, context=apartment_description)
print(extracted_info) # => ApartmentInfo(rent=2500.0 bedrooms=2 bathrooms=1 phone_number='555-123-4567')
```

---

## Questions, Feature Requests?

We hope you find TeapotAI useful and are continuosuly working to improve our models. Please reach out to us on our [Discord](https://discord.gg/hPxGSn5dST) for any technical help or feature requrests. We look forwarding to seeing what our community can build!