import logging
from logging_config import logger
from .base_experiment import BaseExperiment

class LotteryExperiment(BaseExperiment):
    """Lottery-based decision-making experiment."""

    def run(self, agent, config):
        logger.info(f"Running Experiment with {self.agent.model}")
        
        personas_info = config["personas_info"]
        instructions_info = config["instructions_info"]
        rounds_info = config["rounds_info"]
        reasoning = agent.model.reasoning_prompt
        results = []
        id = 0

        for persona_id, persona_desc in personas_info.items():
            id = id
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


                    res, struct_res, selected_option = self.agent.invoke(persona_prompt, prompt)

                    logger.debug(f"Response: {res}") 
                    logger.debug(f"Struct Response: {struct_res}") 

                    results.append({
                        "id_exp": id,
                        "persona": persona_id,
                        "persona desc": persona_desc,
                        "instruction": instruction_id,
                        "instruction desc": instruction_desc,
                        "round": round_id,
                        "round desc": round_desc,
                        "prompt": prompt,
                        "raw_res": res,
                        "struct_res": struct_res,
                        "selected_option": selected_option
                    })
            
                id += 1
        self._log_results(results)
        return results
