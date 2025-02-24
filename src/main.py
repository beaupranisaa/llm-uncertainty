import json
import itertools
import openai
from agents.agent import *
from utils import open_file_as_json, process_lottery_choices
import sys
from agents.reasoning import get_reasoning
import os
from dotenv import load_dotenv
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

sys.path.append("../..")

file_path_persona_info = 'prompt/persona-default.json'
file_path_lottery_choices_instruction = 'prompt/games_instruction-test.json'
file_path_lottery_choices = 'prompt/lottery_choices-test.json'

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

config = {
    "personas_info": personas_info,
    "instructions_info": instructions_info,
    "rounds_info": rounds_info,
    "reasoning": reasoning
}

agent_params = {
    "temperature": 1.0,
    "max_tokens": 1500 #must change
}
# Run agent decisions
# Initialize lottery agent
agent = LotteryAgent(model = "gpt-4-turbo", provider = "openai", **agent_params)
results = agent.run_lottery_decisions(config)

# Save results to a JSON file
os.makedirs("results", exist_ok=True)
with open("results/lottery_results-test-gpt-3.5-turbo-instruct.json", "w") as f:
    json.dump(results, f, indent=4)

print("Lottery choices processed by LLM agent. Results saved to 'lottery_results.json'.")
