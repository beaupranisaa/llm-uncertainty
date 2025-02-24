import openai
import logging
from logging_config import logger
# from transformers import pipeline

class LotteryAgent:

    # List of models that use chat-based inputs
    CHAT_MODELS = {"gpt-3.5-turbo", "gpt-4o", "gpt-4-turbo"}

    def __init__(self, model="gpt-3.5-turbo", provider="openai", **kwargs):
        """
        Initializes the agent with a default model and provider.
        
        Args:
            model (str): Model name (e.g., "gpt-4o", "mistralai/Mistral-7B", "llama-2-13b").
            provider (str): The LLM provider ("openai", "huggingface", "local").
            kwargs: Additional parameters (e.g., temperature, max_tokens).
        """
        self.model = model
        self.provider = provider
        self.params = kwargs  # Store additional parameters dynamically

    def set_model(self, model, provider="openai", **kwargs):
        """
        Dynamically change the model and provider (e.g., OpenAI, Hugging Face, Local).
        """
        self.model = model
        self.provider = provider
        self.params.update(kwargs)  # Update model parameters dynamically

        logger.info(f"🔄 Switching model to: {self.model} (Provider: {self.provider})")

    def query(self, system_prompt="", user_prompt=""):
        """
        Queries the selected LLM provider.

        Args:
            system_prompt (str): Optional system message (for chat-based models).
            user_prompt (str): The main prompt.

        Returns:
            str: Model response or None if an error occurs.
        """
        try:
            if self.provider == "openai":
                return self._query_openai(system_prompt, user_prompt)
            elif self.provider == "huggingface":
                return self._query_huggingface(user_prompt) #Fixed this
            elif self.provider == "local":
                return self._query_local(user_prompt)
            else:
                raise ValueError(f"❌ Unsupported provider: {self.provider}")

        except Exception as e:
            logger.error(f"❌ Error querying {self.model}: {e}")
            return None

    def _query_openai(self, system_prompt, user_prompt):
        """
        Queries OpenAI's models and dynamically selects chat or completion format.
        """
        try:
            if self.model in self.CHAT_MODELS:
                # Use chat format for chat-based models
                response = openai.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    **self.params  # Pass additional parameters dynamically
                )
                return response.choices[0].message.content.strip()
            else:
                # Use completion format for non-chat models
                response = openai.completions.create(
                    model=self.model,
                    prompt=system_prompt + " " + user_prompt,
                    **self.params
                )
                return response.choices[0].text.strip()

        except Exception as e:
            logger.error(f"❌ OpenAI API error: {e}")
            return None

    def _query_huggingface(self, user_prompt):
        """
        Queries a Hugging Face model using the Transformers pipeline.
        """
        # try:
        #     generator = pipeline("text-generation", model=self.model)
        #     response = generator(user_prompt, max_length=self.params.get("max_tokens", 100))
        #     return response[0]["generated_text"].strip()
        # except Exception as e:
        #     logger.error(f"❌ Hugging Face API error: {e}")
        #     return None
        raise NotImplementedError("Huggingface model function to be implemented")


    def _query_local(self, user_prompt):
        """
        Queries a locally hosted LLM (e.g., LLaMA 2, custom fine-tuned models).
        """
        # logger.info(f"🖥️ Running locally: {self.model}")
        # return f"[Simulated response from {self.model}]: {user_prompt}"
        raise NotImplementedError("Local llm function to be implemented")


    def run_lottery_decisions(self, config):

        logger.info(f"Running Experiment of {self.model}, {self.provider}")
        
        personas_info = config["personas_info"]
        instructions_info = config["instructions_info"]
        rounds_info = config["rounds_info"]
        reasoning = config["reasoning"]
        results = []

        for persona_id, persona_desc in personas_info.items():
            # Persona stays the same across all rounds, so define it once
            persona_prompt = "You are a person not an AI model. "
            persona_prompt += persona_desc
            for instruction_id, instruction_desc in instructions_info.items():
                for round_id, round_desc in rounds_info.items():
                    logger.info(f"========= Running Experiment =========")
                    logger.info(f"persona_id: {persona_id}")
                    logger.info(f"instruction_id: {instruction_id}")
                    logger.info(f"round_id: {round_id}")
                    # Reset `prompt` for each round to ensure independence
                    prompt = instruction_desc 
                    prompt += " "
                    prompt += round_desc
                    prompt += reasoning
                    prompt += " You must end with 'Finally, I will choose option ___' ('A' or 'B' are required in the spaces)."

                    decision = self.query(persona_prompt, prompt)

                    logger.debug(f"Decision: {decision}") 

                    results.append({
                        "persona": persona_id,
                        "persona desc": persona_desc,
                        "instruction": instruction_id,
                        "instruction desc": instruction_desc,
                        "round": round_id,
                        "round desc": round_desc,
                        "prompt": prompt,
                        "decision": decision
                    })

        return results