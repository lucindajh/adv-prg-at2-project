import torch
import torchvision as tv
from PIL import Image


model = tv.models.resnet18(pretrained=True)
transform = tv.transforms.Compose([
    tv.transforms.Resize(224),
    tv.transforms.CenterCrop(224),
    tv.transforms.ToTensor(),
    tv.transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])

classes = []
with open("ml/imagenet_classes.txt", "r") as file:
    for line in file:
        classes.append(line.rstrip())
    file.close()


def predict(img: PIL.Image) -> dict:
    """ Makes a prediction on an image
        Args:
            img: PIL image for the prediction
        Returns:
            the class name and probability of the most confident output
    """
    batch_t = torch.unsqueeze(transform(img), 0)

    model.eval()
    out = model(batch_t)

    probabilities = torch.nn.functional.softmax(out, dim=1)[0] * 100
    _, indices = torch.sort(out, descending=True)
    data = {
        'class': classes[indices[0][0]],
        'prob': probabilities[indices[0][0]].item()
    }

    return data



