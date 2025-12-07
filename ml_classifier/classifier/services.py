import logging
from datetime import datetime

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler('../ml_classifier/logs/app.log')
logger.addHandler(file_handler)


def action_logger(func):
    def wrapper(*args, **kwargs):
        user = args[0]
        current_datetime = datetime.now()
        logger.info(f"{current_datetime} - [ACTION] anonymous user is performing {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

