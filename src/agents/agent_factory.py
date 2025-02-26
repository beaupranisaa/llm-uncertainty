from .openai_agent import OpenAIAgent
from .hf_agent import HuggingFaceAgent
from .local_agent import LocalAgent

MODEL_AGENT_MAP = {
    # OpenAI Models
    "gpt-3.5-turbo": OpenAIAgent,
    "gpt-4o-mini": OpenAIAgent,
    "gpt-4o": OpenAIAgent,
    "gpt-4-turbo": OpenAIAgent,
    "gpt-3.5-turbo-instruct": OpenAIAgent,

    # Hugging Face Models
    "mistralai/Mistral-7B": HuggingFaceAgent,
    "meta-llama/Llama-2-13b": HuggingFaceAgent,

    # Local Models
    "custom-llm": LocalAgent
}

class AgentFactory:
    """Factory class to create the correct agent based on the model"""

    @staticmethod
    def get_agent(model, **kwargs):
        AgentClass = MODEL_AGENT_MAP.get(model)
        if not AgentClass:
            raise ValueError(f"❌ Unsupported model: {model}")
        return AgentClass(model, **kwargs)
