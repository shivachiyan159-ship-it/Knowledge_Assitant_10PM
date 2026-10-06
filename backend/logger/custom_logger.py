import os
from datetime import datetime
import logging
import structlog


class CustomLogger:
    # attributes
    # methods
    # constructor
    def __init__(self):
        # 1.create the folder
        self.LOG_FOLDER = os.path.join(os.getcwd(), "logs")
        os.makedirs(self.LOG_FOLDER, exist_ok=True)
        # 2. craete filename path
        LOG_FILE_NAME = f"{datetime.now().strftime("%m_%d_%Y")}.log"
        self.LOG_FILE_PATH = os.path.join(self.LOG_FOLDER, LOG_FILE_NAME)

    def get_logger(self, name=__file__):
        logger_name = os.path.basename(name)

        # output example : c:/users/shiva/custom_logger.py"

        # for file handler
        file_handler = logging.FileHandler(self.LOG_FILE_PATH)
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(logging.Formatter("%(message)s"))

        # for console
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(logging.Formatter("%(message)s"))

        logging.basicConfig(
            level=logging.INFO,
            format="%(message)s",
            handlers=[file_handler, console_handler]
        )

        # configure structlog for JSON structred logging
        structlog.configure(
            processors=[
                structlog.processors.TimeStamper(
                    fmt="iso", utc=True, key="timestamp"),
                structlog.processors.add_log_level,
                structlog.processors.EventRenamer(to="event"),
                structlog.processors.JSONRenderer()
            ],
            logger_factory=structlog.stdlib.LoggerFactory(),
            cache_logger_on_first_use=True
        )

        return structlog.getLogger(logger_name)


# custobj = CustomLogger()
# logger = custobj.get_logger()
# logger.error("zero division error")


if __name__ == "__main__":
    custobj = CustomLogger()
    logger = custobj.get_logger()
    logger.info("i am calling from custom logger")
