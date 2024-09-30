from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.history_aware_retriever import create_history_aware_retriever
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import MessagesPlaceholder
from langchain_chroma.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from llm.llm import get_llm

class QA_chain():
    def __init__(
            self,
            llm: str,
            embedding: str,
            db_directory: str
            ):
        self.llm = get_llm(model=llm),
        self.embedding = HuggingFaceEmbeddings(model_name=embedding),
        self.vector_store = Chroma(
            embedding_function=self.embedding,
            persist_directory=db_directory
            )
        self.retriever = self.vector_store.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 5},
        )
    def answer(self, question:str, chat_history: list):
        contextualize_system_prompt = (
            "给定用户的聊天记录与最新问题。"
            "请你根据聊天记录中的上下文制定一个可以被理解的独立问题。"
            "如果没有聊天记录请不要回答这个问题。"
        )
        contextualize_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", contextualize_system_prompt),
                MessagesPlaceholder("chat_history"),
                ("human", "{input}"),
            ]
        )
        history_aware_retriever = create_history_aware_retriever(
            llm=self.llm,
            retriever=self.retriever,
            prompt=contextualize_prompt
        )
        system_prompt = (
            "你是一个人工智能助手。"
            "请你使用下方检索到的内容来回答问题"
            "如果检索到的内容没有无法用来回答问题，请回复“我不知道”。"
            "\n\n"
            "{context}"
        )
        qa_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                MessagesPlaceholder("chat_history"),
                ("human", "{input}"),
            ]
        )

        question_answer_chain = create_stuff_documents_chain(self.llm, qa_prompt)
        rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)
        response = rag_chain.invoke({"input": question, "chat_history": chat_history})
        return response

