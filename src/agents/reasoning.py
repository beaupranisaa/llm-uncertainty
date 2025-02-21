reasonings = {
    "BDI": "Your answer needs to include the content about your BELIEF, DESIRE, and INTENTION.",
}

def get_reasoning(version="BDI"):
    """Returns the reasoning based on the provided version."""
    return reasonings.get(version, "Default reasoning message: Version not found.")