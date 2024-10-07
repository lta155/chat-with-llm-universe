from langchain_openai import ChatOpenAI
from langchain_community.chat_models import ChatZhipuAI
from .qwen import Qwen2_5_LLM
def get_llm(model: str):
    """
    根据提供的模型名称返回对应的模型实例。
    """
    if model in ["gpt-4o", "gpt-4o-mini", "gpt-4-turbo"]:
        return ChatOpenAI(
            model=model
            )
    elif model in ["glm-4", "glm-4-plus", "glm-4-air"]:
        return ChatZhipuAI(model=model)
    else:
        return Qwen2_5_LLM(model_name_or_path=model)