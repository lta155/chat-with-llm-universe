from langchain_core.prompts import ChatPromptTemplate
from langchain_chroma.vectorstores import Chroma
from langchain_community.embeddings import ZhipuAIEmbeddings
from langchain.chains.history_aware_retriever import create_history_aware_retriever
from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import MessagesPlaceholder
from langchain_core.messages import AIMessage, HumanMessage
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from llm.llm import get_llm

class QA_chain():
    def __init__(
            self,
            llm: str,
            embedding: str,
            db_directory: str,
            k: int
            ):
        self.llm = get_llm(model=llm)
        embedding = ZhipuAIEmbeddings(model=embedding)
        vector_store = Chroma(
            collection_name="llm-universe",
            embedding_function=embedding,
            persist_directory=db_directory
            )
        self.retriever = vector_store.as_retriever(
            search_type="similarity",
            search_kwargs={"k": k},
        )
        self.contextualize_prompt = self._get_contextualize_prompt()
    def answer(self, question:str, chat_history: list):
        chat_history = [HumanMessage(value) if index % 2 == 0 else AIMessage(value) for index, value in enumerate(chat_history)]
        system_prompt = (
            "你是一个问答任务的助手。"
            "请你根据以下检索到的上下文片段来回答问题"
            "如果检索到的片段无法回答问题，就说不知道"
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

        rag_chain = create_retrieval_chain(self.contextualize_prompt, question_answer_chain)
        answer = rag_chain.invoke({"input": question, "chat_history": chat_history})
        return answer["answer"], answer["context"]

    def _get_contextualize_prompt(self):
        contextualize_q_system_prompt = (
            "给定聊天记录和最新的用户问题。"
            "请你根据聊天记录中的上下文制定一个可以被理解的独立问题。"
            "如果没有聊天记录则不用回答这个问题。"
        )

        contextualize_q_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", contextualize_q_system_prompt),
                MessagesPlaceholder("chat_history"),
                ("human", "{input}"),
            ]
        )
        return create_history_aware_retriever(
            self.llm, self.retriever, contextualize_q_prompt
        )