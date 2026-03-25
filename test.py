import torch
import torch.nn as nn
from dataset.dataset_loader import get_loaders
from model.custom_nn import SkinDiseaseCNN
from tqdm import tqdm

def evaluate():
    DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'
    
    # 1. Load Data
    _, _, test_loader, classes = get_loaders()
    
    # 2. Load Model
    model = SkinDiseaseCNN(num_classes=len(classes)).to(DEVICE)
    
    # 3. Load the Final Weights
    checkpoint_path = 'checkpoints/best_model.pth'
    if not torch.os.path.exists(checkpoint_path):
        print(f"❌ Error: {checkpoint_path} not found. Train the model first!")
        return

    checkpoint = torch.load(checkpoint_path, map_location=DEVICE)
    model.load_state_dict(checkpoint['model_state_dict'])
    model.eval()
    
    print(f"✅ Loaded Best Model from Epoch {checkpoint['epoch']} (Val Acc: {checkpoint['acc']:.2f}%)")
    
    # 4. Run Test Set
    correct = 0
    total = 0
    with torch.no_grad():
        for images, labels in tqdm(test_loader, desc="Final Testing"):
            images, labels = images.to(DEVICE), labels.to(DEVICE)
            outputs = model(images)
            _, predicted = outputs.max(1)
            total += labels.size(0)
            correct += predicted.eq(labels).sum().item()
            
    final_acc = 100. * correct / total
    print(f"\n🎯 FINAL TEST ACCURACY: {final_acc:.2f}%")

if __name__ == "__main__":
    evaluate()
