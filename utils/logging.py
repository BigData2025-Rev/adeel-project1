import logging
import os

# Define log file path
LOG_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "app.log")

# Set up logging
logging.basicConfig(
    filename=LOG_FILE,
    filemode="a",
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.DEBUG,
)

# Create a default logger to make importing easier
logger = logging.getLogger()