import logging
import os

logging_format = "[%(asctime)s: %(levelname)s: %(module)s: %(message)s]"
logs_dir = "logs"
os.makedirs(logs_dir,exist_ok=True)
logs_file = os.path.join(logs_dir,"logging.logs")

logging.basicConfig(
    format = logging_format,
    level = logging.INFO,
    handlers=[logging.FileHandler(logs_file)]
)

logger = logging.getLogger("networksecurity")
