from .agent_factory import AgentFactory


class LotteryAgent:
    def __init__(self, model="gpt-3.5-turbo", is_function_call=False, reasoning="BDI", **kwargs):
        """
        Initializes the agent with a selected LLM model.
        
        Args:
            model (str): The name of the LLM model (e.g., "gpt-4o", "mistralai/Mistral-7B").
            function_calling (bool): Whether function calling should be enabled.
            reasoning (str): The reasoning framework to use (e.g., "BDI").
            **kwargs: Additional parameters to configure the model (e.g., temperature, max_tokens).
        """
        self.model = AgentFactory.get_agent(
            model, is_function_call=is_function_call, reasoning=reasoning, **kwargs
        )

    def invoke(self, system_prompt="", user_prompt=""):
        """
        Queries the LLM model and returns a response.
        """
        return self.model.invoke(system_prompt, user_prompt)