import openai
import logging
from logging_config import logger
import json
from .parser import get_struct_output
from .reasoning import get_reasoning
from .function_calls import get_function_calls
from .base_agent import BaseAgent


class OpenAIAgent(BaseAgent):
    """Handles queries to OpenAI models, with optional function calling"""

    CHAT_MODELS = {"gpt-3.5-turbo", "gpt-4o-mini", "gpt-4o", "gpt-4-turbo"}

    def __init__(self, model, is_function_call=False, reasoning="BDI", **params):
        super().__init__(model, **params)  # Call BaseAgent constructor
        self.is_function_call = is_function_call
        self.reasoning = reasoning
        self.reasoning_prompt = get_reasoning(self.reasoning)
    
    def _invoke_chat_fc(self, system_prompt, user_prompt):
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

        if function_response and function_response.name == "lottery_decision_FC":
            res = json.loads(function_response.arguments)
            logger.debug(f"structured_response: {structured_response}")

        return res, res["Final_Option"]
    
    def _invoke_chat_nfc(self, system_prompt, user_prompt):
        response = openai.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            **self.params  # Pass additional parameters dynamically
        )
        
        logger.debug(f"_query_chat_openai_nfc: {response.choices[0].message.content.strip()}")
        res = response.choices[0].message.content.strip()
        return res, get_struct_output(res, self.reasoning)
    
    def _invoke_fc(self, system_prompt, user_prompt):
        raise NotImplementedError("Not yet done")
    
    def _invoke_nfc(self, system_prompt, user_prompt):
        # Use completion format for non-chat models
        response = openai.completions.create(
            model=self.model,
            prompt=system_prompt + " " + user_prompt,
            **self.params
        )
        logger.debug(f"_query_nchat_openai_nfc: {response.choices[0].text.strip()}")
        res = response.choices[0].text.strip()
        return res, get_struct_output(res, self.reasoning)

    def invoke(self, system_prompt, user_prompt):
        try:
            if self.model in self.CHAT_MODELS:
                if self.is_function_call:
                    # chatmodel + fc
                    return self._invoke_chat_fc(system_prompt, user_prompt)
                else:
                    # chatmodel
                    return self._invoke_chat_nfc(system_prompt, user_prompt)
            else:
                if self.is_function_call:
                    # non-chat + fc
                    return self._invoke_fc(system_prompt, user_prompt)
                else:
                    # non-chat
                    return self._invoke_nfc(system_prompt, user_prompt)
        except Exception as e:
            logger.error(f"OpenAI API Error: {e}")
            return None
