import torch
from dataset.dataset_loader import get_loaders
from model.custom_nn import SkinDiseaseModel
from sklearn.metrics import classification_report, confusion_matrix
import os
import numpy as np

def main():
    DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'

    # HAM10000 Classes
    classes = ['akiec', 'bcc', 'bkl', 'df', 'mel', 'nv', 'vasc']
    num_classes = len(classes)

    _, _, test_loader, _ = get_loaders()

    model = SkinDiseaseModel(num_classes=num_classes, pretrained=False).to(DEVICE)

    checkpoint_path = 'checkpoints/best_model.pth'
    if not os.path.exists(checkpoint_path):
        print(f"Error: {checkpoint_path} not found.")
        return

    checkpoint = torch.load(checkpoint_path, map_location=DEVICE)
    model.load_state_dict(checkpoint['model_state_dict'])
    print(f"Loaded Model from Epoch {checkpoint['epoch']} (Val Acc: {checkpoint['acc']:.2f}%)")

    model.eval()
    all_preds = []
    all_labels = []

    with torch.no_grad():
        for images, labels in test_loader:
            images, labels = images.to(DEVICE), labels.to(DEVICE)
            outputs = model(images)
            _, predicted = outputs.max(1)
            
            all_preds.extend(predicted.cpu().numpy())
            all_labels.extend(labels.cpu().numpy())

    print("\n" + "="*50)
    print("CLASSIFICATION REPORT")
    print("="*50)
    print(classification_report(all_labels, all_preds, target_names=classes))
    
    print("\n" + "="*50)
    print("CONFUSION MATRIX")
    print("="*50)
    print(confusion_matrix(all_labels, all_preds))

if __name__ == "__main__":
    main()
