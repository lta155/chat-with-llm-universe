from langchain_text_splitters.markdown import ExperimentalMarkdownSyntaxTextSplitter
from langchain_community.embeddings import ZhipuAIEmbeddings
from langchain_chroma.vectorstores import Chroma
from load_data import ipynb_load, md_load
from tqdm import tqdm
import os

def get_files(dir_path: str) -> list[str]:
    """
    根据给定路径，返回该路径下各文件路径。
    """
    file_list = []
    for filepath, dirnames, filenames in os.walk(dir_path):
        for filename in filenames:
            file_list.append(os.path.join(filepath, filename))
    return file_list


def get_doc(paths: list[str]) -> list[str]:
    """
    根据给定文件路径，返回文件字符串内容。
    """
    doc = []
    for path in paths:
        if path.endswith("md"):
            doc.append(md_load(path=path))
        elif path.endswith("ipynb"):
            doc.append(ipynb_load(path=path))
    return doc


def create_db(dir_path: str, persist_directory: str):
    # 获取 dir_path 下 md 及 ipynb 文件内容
    file_list = get_files(dir_path=dir_path)
    docs = get_doc(file_list)
    # 将获取的docs进行分割
    md_splitter = ExperimentalMarkdownSyntaxTextSplitter()
    for doc in docs:
        splitted_doc = md_splitter.split_text(doc)
    documents  = []
    # 将分割后的代码块合并到之前的内容
    while splitted_doc:
        current_ipynb = splitted_doc.pop(0)
        if "Code" in current_ipynb.metadata:
            documents[-1].page_content += "\n"
            documents[-1].page_content += current_ipynb.page_content
        else:
            documents.append(current_ipynb)
    # 实例化 embedding model
    embedding = ZhipuAIEmbeddings(model="embedding-3")
    # 创建向量数据库
    vector_store = Chroma(
        collection_name="llm-universe",
        embedding_function=embedding,
        persist_directory=persist_directory
    )
    # 定量向数据库中添加内容
    for i in tqdm(range(10, len(documents), 10)):
        vector_store.add_documents(documents=documents[i-10: i])
    vector_store.add_documents(documents=documents[300:])
    return vector_store
if __name__ == "__main__":
    create_db(dir_path="knowledge_db/notebook", persist_directory="knowledge_db/vector_db")