import streamlit as st
from qa_chain.qa_chain import QA_chain

         
def init_session_state():
    """
    初始化 streamlit 中的 session_state 变量
    """
    st.session_state.rag = QA_chain(
        llm="glm-4-plus",
        embedding="embedding-3",
        db_directory="knowledge_db/vector_db",
        k=5
    )
    st.session_state.messages = []
    st.session_state.chat_history = []

# 如果 session_state 中没有 rag 变量，则进行初始化操作
if "rag" not in st.session_state:
    init_session_state()

# 遍历并打印 messages
for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# 在侧边栏中添加 title 及刷新 button
with st.sidebar:
    st.title("🦜🔗 Chat with llm-universe")
    if st.button("Clear chat history"):
        st.session_state.messages = []
        st.session_state.chat_history = []
        st.rerun()

# 添加输入框
user_input = st.chat_input("input your question")

# 若输入框中接收问题，则根据 llm 获取回答并打印召回内容
if user_input:
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.session_state.chat_history.append(user_input)
    
    with st.chat_message("assistant"):
        answer, context = st.session_state.rag.answer(user_input, st.session_state.chat_history)
        st.markdown(answer)
        print(f"问题:\n{user_input}\n")
        for i in range(len(context)):
            print(f"参考信息正文{i + 1}:\n{context[i].page_content}\n")
            print(f"参考信息来源{i + 1}:\n{context[i].metadata}\n")
            print("---" * 10)
        print("*-" * 30)
    st.session_state.messages.append({"role": "assistant", "content": answer})
    st.session_state.chat_history.append(answer)