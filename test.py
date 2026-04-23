import torch
from dataset.dataset_loader import get_loaders
from model.custom_nn import SkinDiseaseModel
import os

def main():
    DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'

    _, _, test_loader, classes = get_loaders()
    num_classes = len(classes)

    model = SkinDiseaseModel(num_classes=num_classes).to(DEVICE)

    checkpoint_path = 'checkpoints/best_model.pth'
    if not os.path.exists(checkpoint_path):
        print(f"Error: {checkpoint_path} not found.")
        return

    checkpoint = torch.load(checkpoint_path, map_location=DEVICE)
    model.load_state_dict(checkpoint['model_state_dict'])
    print(f"Loaded Model from Epoch {checkpoint['epoch']} (Val Acc: {checkpoint['acc']:.2f}%)")

    model.eval()
    correct = 0
    total = 0
    with torch.no_grad():
        for images, labels in test_loader:
            images, labels = images.to(DEVICE), labels.to(DEVICE)
            outputs = model(images)
            _, predicted = outputs.max(1)
            total += labels.size(0)
            correct += predicted.eq(labels).sum().item()

    final_acc = 100. * correct / total
    print(f"FINAL TEST ACCURACY: {final_acc:.2f}%")

if __name__ == "__main__":
    main()
