import openai
import logging
from logging_config import logger

class BaseAgent:
    """Abstract Base Class for LLM models"""
    
    def __init__(self, model, **params):
        self.model = model
        self.params = params  # Store additional parameters dynamically
    
    def invoke(self, system_prompt, user_prompt):
        """Abstract method to be implemented by subclasses"""
        raise NotImplementedError("Each model must implement its own query method.")
