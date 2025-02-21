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
    
open_model_path_dict = {
    ExtendedModelType.VICUNA: "lmsys/vicuna-7b-v1.3",
    ExtendedModelType.LLAMA_2: "meta-llama/Llama-2-7b-chat-hf",
}


sys.path.append("../..")

file_path_character_info = 'prompt/persona-default.json'
file_path_game_instruction = 'prompt/games_instruction.json'
file_path_lottery_choices = 'prompt/lottery_choices.json'

# Get default persona
character_info = open_file_as_json(file_path_character_info)
game_prompts = open_file_as_json(file_path_game_instruction)
game = open_file_as_json(file_path_game)

# Extract character names and information
characters = [f'Persona {i}' for i in range(1, len(character_info) + 1)]
character_info = {f'Persona {i}': info for i, info in enumerate(character_info.values(), start=1)}

# Extract game names and prompts
lottery_choices = {
    prompt[0]: prompt[-1][0] for i, prompt in enumerate(file_path_lottery_choices.values(), start=1)
    } # test only the first one 

games = list(lottery_choices.keys())
print(games)
print(lottery_choices)

# Create dictionary with round as key and formatted string as value
game_round_dict = {}

for i, round_data in enumerate(game["lottery_choices"], start=1):
    option_a = round_data["Option_A"]
    option_b = round_data["Option_B"]

    round_string = (
        f"In option A, there is a {option_a['probability_high']} chance of winning {option_a['reward_high']} "
        f"and {option_a['probability_low']} chance of winning {option_a['reward_low']}. "
        f"In option B, there is a {option_b['probability_high']} chance of winning {option_b['reward_high']} "
        f"and {option_b['probability_low']} chance of winning {option_b['reward_low']}."
    )

    game_round_dict[f"{i}"] = round_string

print("========= game_round_dict ==========")
print(game_round_dict)

model_dict = {
    # 'gpt-3.5-turbo-0613': ExtendedModelType.GPT_3_5_TURBO_0613,
    # 'gpt-3.5-turbo-16k-0613': ExtendedModelType.GPT_3_5_TURBO_16K_0613,
    # 'gpt-4': ExtendedModelType.GPT_4,
    # 'text-davinci-003': ExtendedModelType.INSTRUCT_GPT,
    'gpt-3.5-turbo-instruct': ExtendedModelType.GPT_3_5_TURBO_INSTRUCT,
    # 'vicuna': ExtendedModelType.VICUNA,
    # 'llama-2': ExtendedModelType.LLAMA_2,
}

def update_char_info(char):
    return character_info.get(char, "No information available.")


def update_game_prompt(game):
    return game_prompts.get(game, "No prompt available.")


def process_submission(character, game, question, api_key=None,  model="gpt-3.5-turbo-0613",  extra_prompt="", temperature=1.0, player_demographic=None):
    if api_key is None or api_key == "":
        load_dotenv()
        api_key = os.getenv("OPENAI_API_KEY")
    else:
        os.environ["OPENAI_API_KEY"] = api_key
    return get_res_for_visible(character_info.get(character, ""), game_prompts.get(game, "No prompt available."), game, question, api_key, model_dict[model], extra_prompt, temperature, player_demographic)


if __name__ == "__main__":
    character =""
    game = "lottery_choices"
    api_key = None
    model = "gpt-3.5-turbo-instruct"
    extra_prompt=""
    temperature=1.0
    player_demographic = None
    question = game_round_dict["1"] # first choice

    content = process_submission(character, game, question, api_key, model, extra_prompt, temperature, player_demographic)
    print(content)