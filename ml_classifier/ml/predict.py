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
with open("imagenet_classes.txt", "r") as file:
    for line in file:
        classes.append(line.rstrip())
    file.close()


def predict(image_path: str):
    img = Image.open(image_path)
    batch_t = torch.unsqueeze(transform(img), 0)

    model.eval()
    out = model(batch_t)

    probabilities = torch.nn.functional.softmax(out, dim=1)[0] * 100
    _, indices = torch.sort(out, descending=True)

    return [(classes[idx], probabilities[idx].item()) for idx in indices[0][:5]]



