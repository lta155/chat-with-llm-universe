# chat-with-llm-universe

此项目是基于大语言模型的[llm-universe](https://github.com/datawhalechina/llm-universe)问答助手，是使用langchain 0.3 以 llm-universe 第一部分为主体内容做的RAG应用。如果你想了解更多技术细节见[TECHNICAL_DETAILS.md](https://github.com/lta155/chat-with-llm-universe/blob/main/TECHNICAL_DETAILS.md)

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

## 致谢
[self-llm](https://github.com/datawhalechina/self-llm)：llm接入langchain