import json
import itertools
import openai
from agents.agent import *
from utils import open_file_as_json, process_lottery_choices
import sys
from agents.reasoning import get_reasoning
import os
from dotenv import load_dotenv
import yaml
import logging
from logging_config  import logger# Import logging setup
from utils import get_current_datetime


load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

# Load YAML config
with open("config.yml", "r") as f:
    config = yaml.safe_load(f)

sys.path.append("../..")

file_path_persona_info = config['file_path']['file_path_persona_info']
file_path_lottery_choices_instruction = config['file_path']['file_path_lottery_choices_instruction']
file_path_lottery_choices = config['file_path']['file_path_lottery_choices']

# Get default persona
personas_info_json = open_file_as_json(file_path_persona_info)
print(personas_info_json)
# print(personas_info_json)
# Extract character names and information
personas_info = {f'{i}': info for i, info in enumerate(personas_info_json.values(), start=1)}
print("=========== PERSONA INFO ============")
print(personas_info)

instructions_info_json = open_file_as_json(file_path_lottery_choices_instruction)
instructions_info = {f'{i}': info for i, info in enumerate(instructions_info_json.values(), start=1)}
print("=========== INSTRUCTIONS INFO ============")
print(instructions_info)


round_info_json = open_file_as_json(file_path_lottery_choices)
rounds_info = process_lottery_choices(round_info_json)
print("=========== ROUNDS INFO ============")
print(rounds_info)

reasoning = get_reasoning("BDI")

experiment_config = {
    "personas_info": personas_info,
    "instructions_info": instructions_info,
    "rounds_info": rounds_info,
    "reasoning": reasoning
}

agent_params = {
    "temperature": config['model']['temperature'],
    "max_tokens": config['model']['max_tokens'] #must change
}

model = config['model']['name']
provider = config['model']['provider']

# Run agent decisions
# Initialize lottery agent
agent = LotteryAgent(model = model, provider = provider, **agent_params)
results = agent.run_lottery_decisions(experiment_config)

# Save results to a JSON file
formatted_time = get_current_datetime()

os.makedirs(config['experiment']['output_dir'], exist_ok=True)
output_path = f"{config['experiment']['output_dir']}/{config['experiment']['name']}-test-{model}-{formatted_time}.json"

with open(output_path, "w") as f:
    json.dump(results, f, indent=4)

print(f"Lottery choices processed by LLM agent. Results saved to {output_path}.")
