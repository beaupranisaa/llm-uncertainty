# Default structured response
structured_responses = {
    "BDI" :   {
        "Belief": "Not found",
        "Desire": "Not found",
        "Intention": "Not found",
        "Final_Option": "Not found"
        }
}

function_schemas = { 
    "BDI" : [
        {
            "name": "lottery_decision_FC",
            "description": "Analyzes two lottery options and extracts the user's belief, desire, intention, and final choice.",
            "parameters": {
                "type": "object",
                "properties": {
                    "Belief": {"type": "string", "description": "The belief about the lottery choices."},
                    "Desire": {"type": "string", "description": "The desire in choosing the lottery option."},
                    "Intention": {"type": "string", "description": "The intention behind the lottery decision."},
                    "Final_Option": {
                        "type": "string",
                        "enum": ["Option A", "Option B"],  # Restrict output to only these two
                        "description": "The final choice (Option A or Option B)."
                    }
                },
                "required": ["Belief", "Desire", "Intention", "Final_Option"]
            }
        }
    ]
}

def get_function_calls(version="BDI"):
    """Returns the reasoning based on the provided version."""
    return function_schemas.get(version, "Default reasoning message: Version not found."), structured_responses.get(version, "Default reasoning message: Version not found.")
