import torch
import torch.nn as nn
import torch.optim as optim
from dataset.dataset_loader import get_loaders
from model.custom_nn import SkinDiseaseCNN
from training.trainer import Trainer

def main():
    # --- Config ---
    EPOCHS = 30
    BATCH_SIZE = 32
    LR = 0.0001
    DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'
    
    # --- Data ---
    train_loader, val_loader, _, classes = get_loaders()
    num_classes = len(classes)
    
    # --- Model ---
    model = SkinDiseaseCNN(num_classes=num_classes).to(DEVICE)
    
    # --- Optimization ---
    criterion = nn.CrossEntropyLoss()
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
    print(f"🚀 Starting Training Engine (3-Layer CNN) on {DEVICE}...")
    trainer.fit(epochs=EPOCHS)

if __name__ == "__main__":
    main()
