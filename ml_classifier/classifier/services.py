import logging
from datetime import datetime
from classifier.models import Prediction

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler('../ml_classifier/logs/app.log')
logger.addHandler(file_handler)


def action_logger(func):
    """ wrapper to log function calls """
    def wrapper(*args, **kwargs):
        user = args[0]
        current_datetime = datetime.now()
        logger.info(f"{current_datetime} - [ACTION] anonymous user is performing {func.__name__}")
        return func(*args, **kwargs)
    return wrapper


def read_logs(log_file_path: str):
    """ reads logs line by line from the given log file
    Args:
        log_file_path (str): the file path to read from
    Returns:
        Generator[str]: the file yield
    """
    with open(log_file_path, "r") as file:
        for line in file:
            yield line.strip()


def serialise_prediction(prediction: Prediction) -> dict:
    """ takes a Prediction object and serialises it to a dictionary
    Args:
        prediction (Prediction): the prediction object to serialise
    Returns:
        dict: the dictionary representing the original object
    """
    return {
        "predicted_at": prediction.predicted_at,
        "user": prediction.user,
        "imagenet_class": prediction.imagenet_class,
        "probability": prediction.probability
    }