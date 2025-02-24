import openai

class LotteryAgent:

    def __init__(self, model="gpt-3.5-turbo"):

        self.model = model


    def query_llm(self, system_prompt, user_prompt):
        try:
            response = openai.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=1.0,
                # max_tokens=max_tokens,
                # top_p=top_p,
                # frequency_penalty=frequency_penalty,
                # presence_penalty=presence_penalty
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error querying LLM: {e}")
            return None  # Return None in case of failure

    def run_lottery_decisions(self, config):
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
                    # Reset `prompt` for each round to ensure independence
                    prompt = instruction_desc 
                    prompt += " "
                    prompt += round_desc
                    prompt += reasoning
                    prompt += " You must end with 'Finally, I will choose option ___' ('A' or 'B' are required in the spaces)."

                    decision = self.query_llm(persona_prompt, prompt)

                    print(decision)
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