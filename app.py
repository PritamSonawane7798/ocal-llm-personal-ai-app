import streamlit as st
from personal_knowledge_assistant import PersonalKnowledgeAssistant

st.set_page_config(page_title="Personal Knowledge Assistant", page_icon="🧠")

@st.cache_resource
def load_assistant():
    return PersonalKnowledgeAssistant()

assistant = load_assistant()

st.title("Personal Knowledge Assistant")
st.write("Ask questions about your private documents without sending data to the cloud.")

with st.sidebar:
    st.header("About")
    st.write("""
    This application uses Ollama to run LLMs locally on your machine.
    Your documents and queries never leave your computer.
    """)
    
    model = st.selectbox(
        "Select Model",
        ["llama2", "mistral", "vicuna"]
    )
    assistant.model = model

question = st.text_input("Ask a question:")

if question:
    with st.spinner("Generating answer..."):
        answer = assistant.query(question)
    
    st.write("### Answer")
    st.write(answer)