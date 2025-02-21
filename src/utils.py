
import copy
import json
import os
import sys

import openai
from camel.agents import ChatAgent
from camel.configs import ChatGPTConfig, OpenSourceConfig
from camel.messages import BaseMessage
from camel.types import ModelType, RoleType
from model_class import ExtendedModelType
from dotenv import load_dotenv
import os

def open_file_as_json(file_path):
    with open(file_path, 'r') as file:
        json_file = json.load(file)
    return json_file

def process_lottery_choices(lottery_choices_round_id):
    # Create dictionary with round as key and formatted string as value
    lottery_choices_round_dict = {}

    for i, round_data in enumerate(lottery_choices_round_id["lottery_choices"], start=1):
        option_a = round_data["Option_A"]
        option_b = round_data["Option_B"]

        round_string = (
            f"In option A, there is a {option_a['probability_high']} chance of winning {option_a['reward_high']} "
            f"and {option_a['probability_low']} chance of winning {option_a['reward_low']}. "
            f"In option B, there is a {option_b['probability_high']} chance of winning {option_b['reward_high']} "
            f"and {option_b['probability_low']} chance of winning {option_b['reward_low']}."
        )

        lottery_choices_round_dict[f"{i}"] = round_string
    
    return lottery_choices_round_dict

def str_mes(content):
    return BaseMessage(
        role_name="player",
        role_type=RoleType.USER,
        meta_dict={},
        content=content,
    )


def gpt3_res(prompt, model_name="text-davinci-003", temperature=1):
    response = openai.completions.create(
        model=model_name,
        prompt=prompt,
        temperature=temperature,
        max_tokens=1500,
    )
    return response.choices[0].text.strip()


def get_res_for_visible(
    role,
    first_message,
    game_type,
    question, 
    api_key,
    model_type=ExtendedModelType.GPT_4,
    extra_prompt="",
    temperature=1.0,
    player_demographic=None,
):
    front = "you are a person not an ai model."
    content = ""
    if api_key is not None or api_key != "":
        openai.api_key = api_key
    else:
        openai.api_key = os.getenv("OPENAI_API_KEY")

    extra_prompt  += question
    extra_prompt += "Your answer needs to include the content about your BELIEF, DESIRE and INTENTION."
    if "game" in game_type.lower():
        extra_prompt += "You must end with 'Finally, I will give ___ dollars ' (numbers are required in the spaces)."
    else:
        extra_prompt += "You must end with 'Finally, I will choose option ___' ('A' or 'not B' are required in the spaces)."
    extra_prompt += front

    role = str_mes(role + extra_prompt)
    if player_demographic is not None:
        first_message = first_message.replace(
            "player", player_demographic+" player")
    first_message = str_mes(first_message)
    if model_type in [
        ExtendedModelType.INSTRUCT_GPT,
        ExtendedModelType.GPT_3_5_TURBO_INSTRUCT,
    ]:
        message = role.content + first_message.content + extra_prompt
        final_res = str_mes(gpt3_res(message, model_type.value, temperature))
    else:
        role = str_mes(role.content + extra_prompt)
        model_config = ChatGPTConfig(temperature=temperature)
        if model_type in [
            ModelType.VICUNA,
            ModelType.LLAMA_2,
        ]:
            open_source_config = dict(
                model_type=model_type,
                model_config=OpenSourceConfig(
                    model_path=open_model_path_dict[model_type],
                    server_url="http://localhost:8000/v1",
                    api_params=ChatGPTConfig(temperature=temperature),
                ),
            )
            agent = ChatAgent(
                role, output_language="English", **(open_source_config or {})
            )
        else:
            agent = ChatAgent(
                role,
                model_type=model_type,
                output_language="English",
                model_config=model_config,
            )
        final_all_res = agent.step(first_message)
        final_res = final_all_res.msg
    content += final_res.content

    return content