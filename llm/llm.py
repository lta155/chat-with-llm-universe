from langchain_openai import ChatOpenAI
from .qwen import Qwen2_5_LLM
def get_llm(model: str, api_key: str = None, base_url: str = None):
    if model in ["gpt-4o"]:
        return ChatOpenAI(
            model="gpt-4o",
            api_key = api_key,
            base_url=base_url
            )
    else:
        return Qwen2_5_LLM(model_name_or_path=model)