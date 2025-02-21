reasonings = {
    "BDI": "Your answer needs to include the content about your BELIEF, DESIRE, and INTENTION.",
    "Risk": "Your response should consider the RISK and STRATEGY involved in this decision.",
    "LST": "Think about the possible OUTCOMES and LONG-TERM consequences before making a choice."
}

def get_reasoning(version="BDI"):
    """Returns the reasoning based on the provided version."""
    return reasonings.get(version, "Default reasoning message: Version not found.")