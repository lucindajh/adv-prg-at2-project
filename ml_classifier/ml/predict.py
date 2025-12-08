import torch
import torchvision as tv
from PIL import Image
import logging
from datetime import datetime

from .prediction_observer import PredictionObserver

observer = PredictionObserver()

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler('../ml_classifier/logs/app.log')
logger.addHandler(file_handler)


def log_process(process):
    """ function to log steps in the prediction process
    Args:
        process (str): a message representing the process to log
    """
    logger.info(f"{datetime.now()} - [PREDICT] {process}")


observer.subscribe(log_process)


def predict(img: Image) -> dict:
    """ Makes a prediction on an image
        Args:
            img: PIL image for the prediction
        Returns:
            the class name and probability of the most confident output
    """
    model = tv.models.resnet18(pretrained=True)
    observer.update("model loaded")

    transform = tv.transforms.Compose([
        tv.transforms.Resize(224),
        tv.transforms.CenterCrop(224),
        tv.transforms.ToTensor(),
        tv.transforms.Normalize(
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225]
        )
    ])
    observer.update("created transforms")

    batch_t = torch.unsqueeze(transform(img), 0)

    model.eval()
    out = model(batch_t)
    observer.update("output generated")

    classes = []
    with open("ml/imagenet_classes.txt", "r") as file:
        for line in file:
            classes.append(line.rstrip())
        file.close()
    observer.update("class names loaded")

    probabilities = torch.nn.functional.softmax(out, dim=1)[0] * 100
    _, indices = torch.sort(out, descending=True)
    top_probs = [(classes[idx], probabilities[idx].item()) for idx in indices[0][:5]]
    observer.update(f"probabilities generated. Top probabilities:\n{top_probs}")
    data = {
        'class': classes[indices[0][0]],
        'prob': probabilities[indices[0][0]].item()
    }

    return data



