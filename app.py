import streamlit as st
from llm.llm import get_llm

st.title("🦜🔗 Quickstart App")

st.session_state.qwen_llm = get_llm(model="/sdc/model/Qwen/Qwen2___5-7B-Instruct")

with st.form("my_form"):
    text = st.text_area(
        "Enter text:",
        "What are the three key pieces of advice for learning how to code?",
    )
    submitted = st.form_submit_button("Submit")
    if submitted:
        st.info(st.session_state.qwen_llm.invoke(text))