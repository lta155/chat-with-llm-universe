import json
def ipynb_load(path: str) -> str:
    """
    读取给定路径的 Jupyter Notebook(.ipynb) 文件，提取 markdown 单元格以及 code 单元格内容及输出。
    """
    # 为方便处理，读取文件为 json 格式
    with open(path, "r") as f:
        doc_json = json.load(f)
    texts = ""
    # 遍历单元格
    for cell in doc_json["cells"]:
        if len(cell["source"]) > 0:
            # 将 markdown 单元格内容添加到 texts
            if cell["cell_type"] == "markdown":
                for text in cell["source"]:
                    texts += text
                if len(cell["source"]) == 1:
                    texts += "\n"
            # 将 code 单元格内容添加到 texts
            else:
                # 在 code 单元格内容前后加 markdown 格式
                texts += "\n```python\n"
                for text in cell["source"]:
                    texts += text
                texts += "\n```\n"
                # 将 code 单元格输出添加到 texts
                if len(cell["outputs"]) > 0:
                    texts += "\n```outputs\n"
                    if "text" in cell["outputs"][0]:
                        for output in cell["outputs"][0]["text"]:
                            texts += output
                    elif "text/plain" in cell["outputs"][0]:
                        for output in cell["outputs"][0]["text/plain"]:
                            texts += output
                    texts += "```\n"
    return texts

def md_load(path: str) -> str:
    """
    读取指定路径的 markdown(md) 文件，并返回字符串。
    """
    with open(path, "r") as f:
        texts = f.read()
    return texts