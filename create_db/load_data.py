import json
def ipynb_load(path: str) -> str:
    with open(path, "r") as f:
        doc_json = json.load(f)
    texts = ""
    for cell in doc_json["cells"]:
        if len(cell["source"]) > 0:
            if cell["cell_type"] == "markdown":
                for text in cell["source"]:
                    texts += text
                if len(cell["source"]) == 1:
                    texts += "\n"
            else:
                texts += "\n```python\n"
                for text in cell["source"]:
                    texts += text
                texts += "\n```\n"
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
    with open(path, "r") as f:
        texts = f.read()
    return texts