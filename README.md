# chat-with-llm-universe

此项目是基于大语言模型的[llm-universe](https://github.com/datawhalechina/llm-universe)问答助手，是使用langchain 0.3 以 llm-universe 第一部分为主体内容做的RAG应用。本项目除加载`markdown`及`notebook`文件外均使用`Langchain`框架实现。

<div style="text-align: center;">
<img src="./img/structure.png" alt="solution" width="800">
</div>

## 运行步骤

* api运行，以智谱的`glm-4-plus`与`embedding-3`为例：

    安装相关依赖
    ```bash
    pip install requirements.txt
    ```

    将`.env.template`重命名为`.env`，并在文件中填写智谱AI key。 key可以从[智谱大模型平台](https://open.bigmodel.cn/usercenter/apikeys)获取。

    在命令行中启动streamlit服务

    ```bash
    streamlit run app.py
    ```
* 本地运行：

    安装相关依赖
    ```bash
    pip install requirements_local.txt
    ```
    下载llm权重并接入`langchain`，可以参考[qwen.py](https://github.com/lta155/chat-with-llm-universe/blob/main/llm/qwen.py)。

    本地使用 embedding model，并在[create_db.py](https://github.com/lta155/chat-with-llm-universe/blob/main/create_db/create_db.py)与[qa_chain.py](https://github.com/lta155/chat-with-llm-universe/blob/main/qa_chain/qa_chain.py)中更改`embedding`，可以参考[HuggingFaceEmbeddings](https://api.python.langchain.com/en/latest/embeddings/langchain_huggingface.embeddings.huggingface.HuggingFaceEmbeddings.html#langchain_huggingface.embeddings.huggingface.HuggingFaceEmbeddings)中example。

    构建向量数据库
    ```bash
    python create_db/create_db.py
    ```
    在`app.py`中修改`QA_chain`中相应参数，并在命令行中启动streamlit服务。
    ```bash
    streamlit run app.py
    ```

## 代码结构
```
chat-with-llm-universe/
│
├── create_db/（存放加载文档并构建向量数据库的代码）
│   ├── create_db.py（加载文档并构建向量数据库）
│   └── load_data.py（存放加载文档的函数）
│
├── knowledge_db/（存放llm-universe第一部分及向量数据库）
│   ├── notebook/（存放llm-universe第一部分）
│   │   └── ...
│   └── vector_db/（存放向量数据库）
│       └── ... 
│
├── llm/（存放llm相关内容）
│   ├── llm.py（接入langchain的方法）
│   └── qwen.py（继承langchain的LLM示例）
│
├── qa_chain/（存放检索问答链）
│   └── qa_chain.py（检索问答链）
│
├── .env.template（环境变量模版文件）
│
├── app.py（使用Streamlit部署应用）
│
├── requirements_local.txt
│
├── requirements.txt
```

## 致谢
[self-llm](https://github.com/datawhalechina/self-llm)：llm接入langchain
