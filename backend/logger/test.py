import os
from datetime import datetime
import logging

print(os.getcwd())

print(os.path.join(os.getcwd(), "logs"))
LOG_FOLDER = os.path.join(os.getcwd(), "logs")
os.makedirs(os.path.join(os.getcwd(), "logs"))


print(datetime.now())

# 09_29_2026.log

print(f"{datetime.now().strftime('%m_%d_%Y')}.log")
LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y')}.log"
LOG_FILE_PATH = os.path.join(LOG_FOLDER, LOG_FILE)

logging.basicConfig(
    filename=LOG_FILE_PATH,
    format="[%(asctime)s ] %(levelname)s %(name)s (line:%(lineno)d) - %(message)s",
    level=logging.INFO
)

logger = logging.getLogger(__name__)
logger.error("zero division error")
