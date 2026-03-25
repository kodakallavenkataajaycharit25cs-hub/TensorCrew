import torch
import torch.nn as nn
import torch.optim as optim
from dataset.dataset_loader import get_loaders
from model.custom_nn import SkinDiseaseCNN
from training.trainer import Trainer
from collections import Counter

def main():
    # --- Config ---
    EPOCHS = 30
    BATCH_SIZE = 32
    LR = 0.0002 # Slightly increased for the deeper model
    DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'
    
    # --- Data & Weights ---
    train_loader, val_loader, _, classes = get_loaders()
    num_classes = len(classes)
    
    # Calculate Class Weights to handle Imbalance
    # More weight for small classes, less for big ones.
    print("⚖️ Calculating class weights...")
    targets = [y for _, y in train_loader.dataset.samples]
    count = Counter(targets)
    total_samples = sum(count.values())
    weights = [total_samples / (num_classes * count[i]) for i in range(num_classes)]
    class_weights = torch.FloatTensor(weights).to(DEVICE)
    print(f"✅ Class weights calculated: Min: {min(weights):.2f}, Max: {max(weights):.2f}")
    
    # --- Model ---
    model = SkinDiseaseCNN(num_classes=num_classes).to(DEVICE)
    
    # --- Optimization ---
    # Use the weighted loss!
    criterion = nn.CrossEntropyLoss(weight=class_weights)
    optimizer = optim.Adam(model.parameters(), lr=LR, weight_decay=1e-5)
    scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='min', factor=0.1, patience=3)
    
    # --- Trainer Engine ---
    trainer = Trainer(
        model=model,
        train_loader=train_loader,
        val_loader=val_loader,
        criterion=criterion,
        optimizer=optimizer,
        scheduler=scheduler,
        device=DEVICE,
        save_dir='checkpoints'
    )
    
    # --- Start Training ---
    print(f"🚀 Starting Power Training (4-Layer GAP) on {DEVICE}...")
    trainer.fit(epochs=EPOCHS)

if __name__ == "__main__":
    main()
