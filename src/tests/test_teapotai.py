import pytest
from teapotai import TeapotAI
from pydantic import BaseModel, Field

# Test for the query with context that includes height information
def test_eiffel_tower_height_with_context():
    context = """
    The Eiffel Tower is a wrought iron lattice tower in Paris, France. It was designed by Gustave Eiffel and completed in 1889.
    It stands at a height of 330 meters and is one of the most recognizable structures in the world.
    """
    teapot_ai = TeapotAI()
    answer = teapot_ai.query(query="What is the height of the Eiffel Tower?", context=context)
    assert answer == "The Eiffel Tower stands at a height of 330 meters."

# Test for the query with context that doesn't include height information
def test_eiffel_tower_height_without_context():
    context = """
    The Eiffel Tower is a wrought iron lattice tower in Paris, France. It was designed by Gustave Eiffel and completed in 1889.
    """
    teapot_ai = TeapotAI()
    answer = teapot_ai.query(query="What is the height of the Eiffel Tower?", context=context)
    assert answer == "I don't have information on the height of the Eiffel Tower."

# Test for the chat functionality with RAG (retrieval-augmented generation)
def test_rag_answer_for_landmarks():
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
    teapot_ai = TeapotAI(documents=documents)
    answer = teapot_ai.chat([
        {"role": "system", "content": "You are an agent designed to answer facts about famous landmarks."},
        {"role": "user", "content": "What landmark was constructed in the 1800s?"}
    ])
    assert answer == "The Eiffel Tower was constructed in the 1800s."

# Test for extracting apartment information using a Pydantic model
def test_extract_apartment_info():
    apartment_description = """
    This spacious 2-bedroom apartment is available for rent in downtown New York. The monthly rent is $2500.
    It includes 1 bathrooms and a fully equipped kitchen with modern appliances.

    Pets are welcome!

    Please reach out to us at 555-123-4567 or john@realty.com
    """

    class ApartmentInfo(BaseModel):
        rent: float = Field(..., description="the monthly rent in dollars")
        bedrooms: int = Field(..., description="the number of bedrooms")
        bathrooms: int = Field(..., description="the number of bathrooms")
        phone_number: str

    teapot_ai = TeapotAI()
    extracted_info = teapot_ai.extract(ApartmentInfo, context=apartment_description)

    assert extracted_info.rent == 2500.0
    assert extracted_info.bedrooms == 2
    assert extracted_info.bathrooms == 1
    assert extracted_info.phone_number == '555-123-4567'
