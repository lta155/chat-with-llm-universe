import streamlit as st
from qa_chain.qa_chain import QA_chain
with st.sidebar:
    st.title("🦜🔗 Chat with llm-universe")

def init_session_state():
    st.session_state.rag = QA_chain(
        llm="/sdc/model/Qwen/Qwen2___5-7B-Instruct",
        embedding="/sdc/model/models--TencentBAC--Conan-embedding-v1/snapshots/fbdfbc53cd9eff1eb55eadc28d99a9d4bff4135f",
        db_directory="knowledge_db/vector_db"
    )
    st.session_state.messages = []
    st.session_state.chat_history = []

if "rag" not in st.session_state:
    init_session_state()

for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

user_input = st.chat_input("input your question")

if user_input:
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.session_state.chat_history.append(user_input)
    
    with st.chat_message("assistant"):
        answer = st.session_state.rag.answer(user_input, st.session_state.chat_history)
        st.markdown(answer)
    st.session_state.messages.append({"role": "assistant", "content": answer})
    st.session_state.chat_history.append(answer)