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
        valid_options = {"Option A", "Option B", "option A", "option B"}  # Allowed values
        if value not in valid_options:
            return None  # If not valid, return None
        return value  # Otherwise, return the valid option

def get_struct_output(input, reasoning = "BDI", test=False):
    if test:
        return (1, {})
    
    if reasoning == "BDI":
        response_mod = BDI_option_extract
    else:
        logger.error(f"❌ Error Unsupported {reasoning}: {e}")
    
    logger.debug(f"Input: {input}")
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

