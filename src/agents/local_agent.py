from .base_agent import BaseAgent

class LocalAgent(BaseAgent):
    """Handles local models (e.g., LLaMA, custom fine-tuned models)"""

    def query(self, system_prompt, user_prompt):
        raise NotImplementedError("Local model function to be implemented")
