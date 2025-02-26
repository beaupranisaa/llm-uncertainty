import openai
import logging
from logging_config import logger
import json
from .parser import get_struct_output
from .reasoning import get_reasoning
from .function_calls import get_function_calls
# from transformers import pipeline

class LotteryAgent:

    # List of models that use chat-based inputs
    CHAT_MODELS = {"gpt-3.5-turbo",  "gpt-4o-mini", "gpt-4o", "gpt-4-turbo"}

    def __init__(self, model="gpt-3.5-turbo", provider="openai", is_function_call = False, reasoning = "BDI", **kwargs):
        """
        Initializes the agent with a default model and provider.
        
        Args:
            model (str): Model name (e.g., "gpt-4o", "mistralai/Mistral-7B", "llama-2-13b").
            provider (str): The LLM provider ("openai", "huggingface", "local").
            kwargs: Additional parameters (e.g., temperature, max_tokens).
        """
        self.model = model
        self.provider = provider
        self.is_function_call = is_function_call
        self.reasoning = reasoning
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
                return self._query_huggingface(system_prompt, user_prompt) #Fixed this
            elif self.provider == "local":
                return self._query_local(system_prompt, user_prompt)
            elif self.provider == "test":
                return self._query_test(system_prompt, user_prompt)
            else:
                raise ValueError(f"❌ Unsupported provider: {self.provider}")

        except Exception as e:
            logger.error(f"❌ Error querying {self.model}: {e}")
            return None

    def _query_chat_openai_fc(self, system_prompt, user_prompt):
        # TODO: only works with BDI, not flexi enough
        lottery_function_schema, structured_response = get_function_calls(self.reasoning)
        response = openai.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            functions=lottery_function_schema,  # Register function
            function_call= {"name": lottery_function_schema[0]['name']}, #"auto",  # Let GPT decide when to call the function
            **self.params  # Pass additional parameters dynamically
        )

        # Extract the function call response
        function_response = response.choices[0].message.function_call

        logger.debug(f"-----------------------------")
        logger.debug(f"function_response: {function_response}")
        
\
        print("function response name: ", function_response.name)

        if function_response and function_response.name == "lottery_decision_FC":
            structured_response = json.loads(function_response.arguments)
\
        # logger.debug(f"full_response: {full_response}")
        logger.debug(f"structured_response: {structured_response}")

        return structured_response
    
    def _query_chat_openai_nfc(self, system_prompt, user_prompt):

        response = openai.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            **self.params  # Pass additional parameters dynamically
        )
        
        logger.debug(f"_query_chat_openai_nfc: {response.choices[0].message.content.strip()}")
        return response.choices[0].message.content.strip()
    
    def _query_nchat_openai_nfc(self, system_prompt, user_prompt):
        # Use completion format for non-chat models
        response = openai.completions.create(
            model=self.model,
            prompt=system_prompt + " " + user_prompt,
            **self.params
        )
        logger.debug(f"_query_nchat_openai_nfc: {response.choices[0].text.strip()}")
        return response.choices[0].text.strip()


    def _query_openai(self, system_prompt, user_prompt):
        """
        Queries OpenAI's models and dynamically selects chat or completion format.
        """
        try:
            if self.model in self.CHAT_MODELS:
                # Use chat format for chat-based models
                if self.is_function_call:
                    # Use chat format for chat-based models + function_calls
                    res = self._query_chat_openai_fc(system_prompt, user_prompt)
                    return res, res["Final_Option"]

                else:
                    logger.debug(f"model: {self.model}")
                    logger.debug(f"""function_calls: {self.is_function_call}""")
                    # Use chat format for chat-based models + no function_calls
                    res = self._query_chat_openai_nfc(system_prompt, user_prompt)
                    return res, get_struct_output(res, self.reasoning)
            else:
                # Use completion format for non-chat models
                return self._query_nchat_openai_nfc(system_prompt, user_prompt)

        except Exception as e:
            logger.error(f"❌ OpenAI API error: {e}")
            return None

    def _query_huggingface(self,system_prompt, user_prompt):
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


    def _query_local(self, system_prompt, user_prompt):
        """
        Queries a locally hosted LLM (e.g., LLaMA 2, custom fine-tuned models).
        """
        # logger.info(f"🖥️ Running locally: {self.model}")
        # return f"[Simulated response from {self.model}]: {user_prompt}"
        raise NotImplementedError("Local llm function to be implemented")
        
    def _query_test(self, system_prompt, user_prompt):
        """
        Queries a locally hosted LLM (e.g., LLaMA 2, custom fine-tuned models).
        """
        # logger.info(f"🖥️ Running locally: {self.model}")
        prompt = system_prompt + " " + user_prompt
        return f"[Simulated response from {self.model}]: {prompt}"
        # raise NotImplementedError("Local llm function to be implemented")

    def run_lottery_decisions(self, config):

        logger.info(f"Running Experiment of {self.model}, {self.provider}")
        
        personas_info = config["personas_info"]
        instructions_info = config["instructions_info"]
        rounds_info = config["rounds_info"]
        reasoning = get_reasoning("BDI")
        results = []

        for persona_id, persona_desc in personas_info.items():
            # Persona stays the same across all rounds, so define it once
            persona_prompt = "You are a person not an AI model. "
            persona_prompt += persona_desc
            logger.debug(f"persona_prompt: {persona_prompt}") 
            for instruction_id, instruction_desc in instructions_info.items():
                logger.debug(f"instruction_desc: {instruction_desc}") 
                for round_id, round_desc in rounds_info.items():
                    logger.debug(f"round_desc: {round_desc}") 
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

                    # return both parsed output and not parsed
                    res, struct_res = self.query(persona_prompt, prompt)

                    # final_answer = self.select(decision) choices=['OptionA', 'Option B']

                    logger.debug(f"Response: {res}") 
                    logger.debug(f"Struct Response: {struct_res}") 

                    results.append({
                        "persona": persona_id,
                        "persona desc": persona_desc,
                        "instruction": instruction_id,
                        "instruction desc": instruction_desc,
                        "round": round_id,
                        "round desc": round_desc,
                        "prompt": prompt,
                        "raw_res": res,
                        "struct_res": struct_res
                    })

        return results