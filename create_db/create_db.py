from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders.notebook import NotebookLoader
from langchain_community.document_loaders.markdown import UnstructuredMarkdownLoader
from langchain_text_splitters.markdown import MarkdownTextSplitter
from langchain_text_splitters.character import RecursiveCharacterTextSplitter
from langchain_chroma.vectorstores import Chroma
from spilt import spilt_ipynb
import os

def get_files(dir_path: str):
    file_list = []
    for filepath, dirnames, filenames in os.walk(dir_path):
        for filename in filenames:
            file_list.append(os.path.join(filepath, filename))
    return file_list


def get_doc(paths: list[str]):
    md_loaders = []
    ipynb_loaders = []
    for path in paths:
        if path.endswith("md"):
            md_loaders.append(UnstructuredMarkdownLoader(file_path=path))
        elif path.endswith("ipynb"):
            ipynb_loaders.append(NotebookLoader(path=path))
    md_docs = [md_loader.load() for md_loader in md_loaders]
    ipynb_docs = [ipynb_loader.load() for ipynb_loader in ipynb_loaders]
    return md_docs, ipynb_docs

def get_emb(model_name_path: str):
    return HuggingFaceEmbeddings(model_name=model_name_path)
def create_db(dir_path: str, persist_directory: str):
    file_list = get_files(dir_path=dir_path)
    md_docs, ipynb_docs = get_doc(file_list)
    md_splitter = MarkdownTextSplitter(
        chunk_size=400,
        chunk_overlap=100
    )
    splited_md = md_splitter.split_documents(md_docs)
    separators = [
    "'markdown' cell",
    "'code' cell",
    "/n/n",
    "/n",
    " "
    ]
    ipynb_splitter = RecursiveCharacterTextSplitter(
        chunk_size=400,
        chunk_overlap=100,
        separators=separators,
        keep_separator=True
    )
    splited_ipynb = ipynb_splitter.split_documents(ipynb_docs)
    documents = []
    documents.extend(splited_md)
    documents.extend(splited_ipynb)
    embedding = HuggingFaceEmbeddings(model_name="/sdc/model/models--TencentBAC--Conan-embedding-v1/snapshots/fbdfbc53cd9eff1eb55eadc28d99a9d4bff4135f")

get_emb("/sdc/model/models--TencentBAC--Conan-embedding-v1/snapshots/fbdfbc53cd9eff1eb55eadc28d99a9d4bff4135f")