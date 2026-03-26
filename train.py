import torch
import torch.nn as nn
import torch.optim as optim
from dataset.dataset_loader import get_loaders
from model.custom_nn import SkinDiseaseCNN
from training.trainer import Trainer
from collections import Counter
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--resume", action="store_true", help="Resume from checkpoint")
    args = parser.parse_args()

    EPOCHS = 100
    LR = 0.0003
    DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'
    
    train_loader, val_loader, test_loader, classes = get_loaders()
    num_classes = len(classes)
    
    print("⚖️ Calculating class weights...")
    targets = [y for _, y in train_loader.dataset.samples]
    count = Counter(targets)
    total_samples = sum(count.values())
    weights = [total_samples / (num_classes * count[i]) for i in range(num_classes)]
    class_weights = torch.FloatTensor(weights).to(DEVICE)
    
    model = SkinDiseaseCNN(num_classes=num_classes).to(DEVICE)
    
    criterion = nn.CrossEntropyLoss(weight=class_weights)
    optimizer = optim.Adam(model.parameters(), lr=LR, weight_decay=1e-4)
    scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='min', factor=0.5, patience=5)
    
    trainer = Trainer(
        model=model,
        train_loader=train_loader,
        test_loader=val_loader, # Using val_loader as test for evaluation during training
        criterion=criterion,
        optimizer=optimizer,
        scheduler=scheduler,
        device=DEVICE
    )
    
    start_epoch = 0
    if args.resume:
        start_epoch = trainer.load_checkpoint()

    print(f"🚀 Training 4-Layer ResNet-Custom on {DEVICE}...")
    trainer.train(epochs=EPOCHS, start_epoch=start_epoch)

if __name__ == "__main__":
    main()
