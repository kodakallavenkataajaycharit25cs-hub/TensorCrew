import sys
import torch
import torch.nn as nn
import torch.optim as optim
from pathlib import Path
from tqdm import tqdm

root_path = Path(__file__).resolve().parents[1]
sys.path.append(str(root_path))

from model.custom_nn import SkinDiseaseCNN
from dataset.dataset_loader import get_loaders

def train_one_epoch(model, loader, optimizer, criterion, device):
    model.train()
    running_loss = 0.0
    correct = 0
    total = 0

    pbar = tqdm(loader, desc="  Training")
    for images, labels in pbar:
        images, labels = images.to(device), labels.to(device)

        optimizer.zero_grad()
        outputs = model(images)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        running_loss += loss.item()
        _, predicted = outputs.max(1)
        total += labels.size(0)
        correct += predicted.eq(labels).sum().item()

        pbar.set_postfix({"Loss": f"{loss.item():.4f}", "Acc": f"{100.*correct/total:.2f}%"})

    return running_loss / len(loader), 100. * correct / total

def validate(model, loader, criterion, device):
    model.eval()
    running_loss = 0.0
    correct = 0
    total = 0

    with torch.no_grad():
        pbar = tqdm(loader, desc="  Validating")
        for images, labels in pbar:
            images, labels = images.to(device), labels.to(device)
            outputs = model(images)
            loss = criterion(outputs, labels)

            running_loss += loss.item()
            _, predicted = outputs.max(1)
            total += labels.size(0)
            correct += predicted.eq(labels).sum().item()
            
            pbar.set_postfix({"Loss": f"{loss.item():.4f}", "Acc": f"{100.*correct/total:.2f}%"})

    return running_loss / len(loader), 100. * correct / total

def main():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"🚀 Training on: {device}")

    # Hyperparameters
    LEARNING_RATE = 0.001
    EPOCHS = 20
    # Save the model in the 'model' directory
    SAVE_PATH = root_path / "model" / "best_skin_model.pth"

    train_loader, val_loader, test_loader, classes = get_loaders()
    model = SkinDiseaseCNN(num_classes=len(classes)).to(device)
    
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=LEARNING_RATE)

    best_acc = 0.0
    print(f"🎬 Starting training for {len(classes)} classes...")

    for epoch in range(EPOCHS):
        print(f"\n✨ Epoch {epoch+1}/{EPOCHS}")
        
        train_loss, train_acc = train_one_epoch(model, train_loader, optimizer, criterion, device)
        val_loss, val_acc = validate(model, val_loader, criterion, device)
        
        print(f" Train Loss: {train_loss:.4f} | Train Acc: {train_acc:.2f}%")
        print(f" Val Loss:   {val_loss:.4f} | Val Acc:   {val_acc:.2f}%")

        if val_acc > best_acc:
            best_acc = val_acc
            torch.save(model.state_dict(), SAVE_PATH)
            print(f"🏆 New Best Model Saved! (Acc: {best_acc:.2f}%)")

    print(f"\n🎉 Training Finished! Best Validation Accuracy: {best_acc:.2f}%")

if __name__ == "__main__":
    main()
