import pytest
from teapotai import TeapotAI


@pytest.fixture(scope="module")
def model():
    return TeapotAI()


def test_basic_question(model):
    response = model("What is the capital of Italy?")
    assert isinstance(response, str)
    assert len(response) > 0


def test_question_with_context(model):
    context = """
    Italy is a country in Europe. Its capital is known for its history, food, and architecture.
    """
    response = model(
        "What is the capital?",
        context=context
    )
    assert isinstance(response, str)
    assert "Rome" in response or len(response) > 0


def test_multiple_choice_format(model):
    context = "Water boils at a specific temperature under standard conditions."
    question = "At what temperature does water boil?"
    options = ["50°C", "100°C", "150°C"]
    response = model(
        question,
        context=context,
        options=options
    )
    assert isinstance(response, str)
    assert any(opt in response for opt in options)


def test_bullet_point_answer_format(model):
    context = """
    Apples are red or green. Bananas are yellow. Grapes can be red or green or purple.
    """
    question = "List the fruits and their colors."
    response = model(question, context=context)
    assert isinstance(response, str)
    assert "-" in response or "•" in response  # Bullet points
    assert "apple" in response.lower() or "banana" in response.lower()


def test_question_answering_style(model):
    context = "The mitochondria is the powerhouse of the cell."
    response = model("What is the mitochondria?", context=context)
    assert isinstance(response, str)
    assert len(response) > 0


def test_code_formatting(model):
    question = "Write a Python function to add two numbers."
    response = model(question)
    assert isinstance(response, str)
    assert "def" in response and "add" in response


def test_edge_case_empty_question(model):
    response = model("")
    assert isinstance(response, str)


def test_edge_case_long_context(model):
    context = "Dog. " * 1000  # Very long context
    question = "What is the repeated word?"
    response = model(question, context=context)
    assert isinstance(response, str)
    assert "Dog" in response or "dog" in response


def test_boolean_output(model):
    question = "Is the sky blue?"
    response = model(question)
    assert isinstance(response, str)
    assert "yes" in response.lower() or "no" in response.lower()


def test_math_question(model):
    question = "What is 12 times 8?"
    response = model(question)
    assert isinstance(response, str)
    # Don't assert correctness, just that it runs and is numeric-ish
    assert any(char.isdigit() for char in response)
