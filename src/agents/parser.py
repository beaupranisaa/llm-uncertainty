import json
import os
import time

import instructor
import openai
import pydantic_core
import tqdm
from openai import OpenAI
from typing import Optional
from pydantic import BaseModel, field_validator
import logging
from logging_config import logger

client = instructor.patch(OpenAI(api_key=os.getenv("OPENAI_API_KEY")))

class BDI_option_extract(BaseModel):
    #TODO: still not dynamic
    belief: Optional[str] = "Unknown"  # Uses "Unknown" if missing
    desire: Optional[str] = "Unknown"
    intention: Optional[str] = "Unknown"
    selected_option: Optional[str] = None  # Defaults to None if not present

    @field_validator("selected_option", mode="before")
    @classmethod
    def validate_selected_option(cls, value):
        valid_options = {
            "Option A": "A", "option A": "A", "A": "A",
            "Option B": "B", "option B": "B", "B": "B"
        }
        normalized_value = valid_options.get(value.strip(), None)  # Normalize or return None
        if normalized_value is None:
            logger.debug(f"Invalid selected option: {value}")
        return normalized_value

def transform_output(input, response_mod):
    
    if response_mod.__name__ == "BDI_option_extract":
        # Mapping the original structure to the new structure
        belief_mapping = input.get("Belief", "").strip()
        desire_mapping = input.get("Desire", "").strip()
        intention_mapping = input.get("Intention", "").strip()

        selected_option = input.get("Final_Option", "").strip()
        logger.debug(f"selected_option {selected_option}")

        
        transformed_data = response_mod(
            belief=belief_mapping,
            desire=desire_mapping,
            intention=intention_mapping,
            selected_option=f"{selected_option}"
        )
        return transformed_data
    else:
        logger.error(f"❌ Error Unsupported {reasoning}: {e}")

def get_struct_output(input, reasoning = "BDI", is_chat = False, test=False):
    if test:
        return (1, {})
    
    if reasoning == "BDI":
        response_mod = BDI_option_extract
    else:
        logger.error(f"❌ Error Unsupported {reasoning}: {e}")
    
    logger.debug(f"Input: {input}")

    if is_chat:
        resp = transform_output(input, response_mod)
    else:
        resp = client.chat.completions.create(
            model="gpt-4o-mini",  # TODO change if you need
            response_model=response_mod,
            messages=[
                {"role": "user", "content": input},
            ],
        )

        logger.debug(f"Output from get_struct_output {resp}")

    if response_mod.__name__ == "BDI_option_extract":
        option_extracted = resp.selected_option
        return (
            option_extracted,
            dict(resp),
        )
    else:
        logger.error(f"❌ Error Returning {reasoning} Unsupported: {e}")

