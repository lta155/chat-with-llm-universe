from langchain_text_splitters.markdown import ExperimentalMarkdownSyntaxTextSplitter
from langchain_community.embeddings import ZhipuAIEmbeddings
from langchain_chroma.vectorstores import Chroma
from load_data import ipynb_load, md_load
from tqdm import tqdm
import os

def get_files(dir_path: str):
    file_list = []
    for filepath, dirnames, filenames in os.walk(dir_path):
        for filename in filenames:
            file_list.append(os.path.join(filepath, filename))
    return file_list


def get_doc(paths: list[str]) -> list[str]:
    doc = []
    for path in paths:
        if path.endswith("md"):
            doc.append(md_load(path=path))
        elif path.endswith("ipynb"):
            doc.append(ipynb_load(path=path))
    return doc


def create_db(dir_path: str, persist_directory: str):
    file_list = get_files(dir_path=dir_path)
    docs = get_doc(file_list)
    md_splitter = ExperimentalMarkdownSyntaxTextSplitter()
    for doc in docs:
        splitted_doc = md_splitter.split_text(doc)
    documents  = []
    while splitted_doc:
        current_ipynb = splitted_doc.pop(0)
        if "Code" in current_ipynb.metadata:
            documents[-1].page_content += "\n"
            documents[-1].page_content += current_ipynb.page_content
        else:
            documents.append(current_ipynb)
    embedding = ZhipuAIEmbeddings(model="embedding-3")
    vector_store = Chroma(
        collection_name="llm-universe",
        embedding_function=embedding,
        persist_directory=persist_directory
    )
    for i in tqdm(range(10, len(documents), 10)):
        vector_store.add_documents(documents=documents[i-10: i])
    vector_store.add_documents(documents=documents[300:])
    return vector_store
if __name__ == "__main__":
    create_db(dir_path="knowledge_db/notebook", persist_directory="knowledge_db/vector_db")