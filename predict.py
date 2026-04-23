import torch
import torch.nn.functional as F
from torchvision import transforms
from PIL import Image
from model.custom_nn import SkinDiseaseModel
from dataset.dataset_loader import get_loaders
import os

def predict(image_path):
    DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'

    _, _, _, classes = get_loaders()
    num_classes = len(classes)

    model = SkinDiseaseModel(num_classes=num_classes).to(DEVICE)
    checkpoint_path = 'checkpoints/best_model.pth'
    
    if not os.path.exists(checkpoint_path):
        print("Error: Model checkpoint not found.")
        return

    checkpoint = torch.load(checkpoint_path, map_location=DEVICE)
    model.load_state_dict(checkpoint['model_state_dict'])
    model.eval()

    transform = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
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
