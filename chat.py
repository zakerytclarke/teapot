import streamlit as st
from teapotai import TeapotAI

# Function to handle the chat with TeapotAI
def handle_chat(user_input, teapot_ai):
    response = teapot_ai.chat([
        {
            "role": "system",
            "content": "You are an agent designed to answer facts about famous landmarks."
        },
        {
            "role": "user",
            "content": user_input
        }
    ])
    return response

# Streamlit app
def main():
    st.set_page_config(page_title="TeapotAI Chat", page_icon=":robot_face:", layout="wide")

    # Header with the image and description
    st.title("Teapot AI")
    st.image("https://teapotai.com/assets/logo.gif", width=150)  # Adjust size to your preference
    st.markdown("""
    [Website](https://teapotai.com/) | [Demo](https://huggingface.co/spaces/teapotai/teapotchat) | [Discord](https://discord.gg/hPxGSn5dST)
    
    Teapot is a small open-source language model (~300 million parameters) fine-tuned on synthetic data and optimized to run locally on resource-constrained devices such as smartphones and CPUs. Teapot can perform a variety of tasks, including hallucination-resistant Question Answering (QnA), Retrieval-Augmented Generation (RAG), and JSON extraction. Teapot is a model built by and for the community.
    """)

    # Sidebar for document input
    st.sidebar.header("Document Input (for RAG)")
    user_documents = st.sidebar.text_area(
        "Enter documents as a JSON list of strings (e.g., [\"Document 1\", \"Document 2\"])",
        value='["The Eiffel Tower is located in Paris, France. It was built in 1889 and stands 330 meters tall.", "The Great Wall of China is a historic fortification that stretches over 13,000 miles."]'
    )

    # Parse the user input to get the documents (make sure it's valid JSON)
    try:
        documents = eval(user_documents)
        if not isinstance(documents, list) or not all(isinstance(doc, str) for doc in documents):
            raise ValueError("Invalid input: Must be a JSON array of strings.")
    except Exception as e:
        st.sidebar.error(f"Error parsing documents: {e}")
        documents = []  # Fallback to empty documents in case of error

    # Initialize TeapotAI with the user-defined documents
    if documents:
        teapot_ai = TeapotAI(documents=documents)
    else:
        teapot_ai = TeapotAI(documents=["The Eiffel Tower is located in Paris, France. It was built in 1889 and stands 330 meters tall."])

    # Initialize chat history if not already present
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display previous messages from chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accept user input
    user_input = st.chat_input("Ask about famous landmarks:")

    if user_input:
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(user_input)

        # Add user message to session state
        st.session_state.messages.append({"role": "user", "content": user_input})

        # Get the answer from TeapotAI using chat functionality
        response = handle_chat(user_input, teapot_ai)

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            st.markdown(response)

        # Add assistant response to session state
        st.session_state.messages.append({"role": "assistant", "content": response})

# Run the app
if __name__ == "__main__":
    main()
