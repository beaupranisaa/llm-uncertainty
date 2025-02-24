import yaml
import logging
from utils import get_current_datetime
import os

# Load YAML config
with open("config.yml", "r") as f:
    config = yaml.safe_load(f)

# Set logging level
log_level = config["logging"]["level"].upper()
print("=== LOG LEVEL ====",log_level)

log_levels = {
    "DEBUG": logging.DEBUG, 
    "INFO": logging.INFO, 
    "WARNING": logging.WARNING, 
    "ERROR": logging.ERROR
    }

formatted_time = get_current_datetime()

log_file = f"{config['logging']['log_dir']}/{config['experiment']['name']}-test-{config['model']['name']}-{formatted_time}.log"

os.makedirs(config['logging']['log_dir'], exist_ok=True)

# Create logger
logger = logging.getLogger("experiment_logger")
logger.setLevel(log_levels.get(log_level, logging.INFO))  # Set global log level\
logger.propagate = True

# Create file handler (logs everything)
file_handler = logging.FileHandler(log_file)
file_handler.setLevel(logging.DEBUG)  # Store all logs in file

# Create console handler (logs only INFO and above)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)  # Avoid cluttering terminal with DEBUG logs

# Define log format
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add handlers to logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# Test log message
logger.info("Logging initialized! Logs will be written to both file and terminal.")
