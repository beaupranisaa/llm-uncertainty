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

open_model_path_dict = {
    ModelType.VICUNA: "lmsys/vicuna-7b-v1.3",
    ModelType.LLAMA_2: "meta-llama/Llama-2-7b-chat-hf",
}
front = "you are a person not an ai model."


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


sys.path.append("../..")

file_path_character_info = 'prompt/persona-default.json'
file_path_game_instruction = 'prompt/games_instruction.json'
file_path_game = 'prompt/games.json'

# Get default persona
with open(file_path_character_info, 'r') as file:
    character_info = json.load(file)

# Load game prompts
with open(file_path_game_instruction, 'r') as file:
    game_prompts = json.load(file)

# Load game 
with open(file_path_game, 'r') as file:
    game = json.load(file)

# Extract character names and information
characters = [f'Persona {i}' for i in range(
    1, len(character_info) + 1)]
character_info = {f'Persona {i}': info for i, info in enumerate(
    character_info.values(), start=1)}

# Extract game names and prompts
game_prompts = {
    prompt[0]: prompt[-1][0] for i, prompt in enumerate(game_prompts.values(), start=1)} # test only the first one 
games = list(game_prompts.keys())
print(games)
print(game_prompts)

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


models = list(model_dict.keys())


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


# # Load .env file
# load_dotenv()

# # Access environment variables
# openai_api_key = os.getenv("OPENAI_API_KEY")


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