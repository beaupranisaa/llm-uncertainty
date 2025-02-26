from .base_agent import BaseAgent

class HuggingFaceAgent(BaseAgent):
    """Handles Hugging Face models"""
    
    def query(self, system_prompt, user_prompt):
        raise NotImplementedError("Hugging Face model function to be implemented")
