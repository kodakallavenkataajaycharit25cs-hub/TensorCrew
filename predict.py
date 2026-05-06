import torch
import torch.nn.functional as F
from torchvision import transforms
from PIL import Image
from model.custom_nn import SkinDiseaseModel
from dataset.dataset_loader import get_loaders
import os

def predict(image_path):
    DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'

    num_classes = 7
    model = SkinDiseaseModel(num_classes=num_classes, pretrained=False).to(DEVICE)
    
    # HAM10000 normalization
    MEAN = [0.763, 0.546, 0.570]
    STD = [0.141, 0.153, 0.169]

    transform = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(MEAN, STD)
    ])

    image = Image.open(image_path).convert('RGB')
    image = transform(image).unsqueeze(0).to(DEVICE)

    with torch.no_grad():
        output = model(image)
        prob = F.softmax(output, dim=1)
        conf, pred = torch.max(prob, 1)

    print(f"PREDICTION FOR: {image_path}")
    print(f"Disease: {classes[pred.item()]}")
    print(f"Confidence: {100*conf.item():.2f}%")

if __name__ == "__main__":
    predict('test_image.jpg')
