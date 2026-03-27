import torch
import torch.nn as nn
import torch.optim as optim
from dataset.dataset_loader import get_loaders
from model.custom_nn import SkinDiseaseResNet
from training.trainer import Trainer
from collections import Counter
import os

def main():
    # --- Config ---
    EPOCHS = 20 
    BATCH_SIZE = 32
    LR = 0.0001 
    DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'

    if not os.path.exists('checkpoints'):
        os.makedirs('checkpoints')

    # --- Data ---
    train_loader, val_loader, _, classes = get_loaders()
    num_classes = len(classes)

    # Class Weights
    print("⚖️ Calculating class weights...")
    targets = [y for _, y in train_loader.dataset.samples]
    count = Counter(targets)
    total_samples = sum(count.values())
    weights = [total_samples / (num_classes * count[i]) for i in range(num_classes)]
    class_weights = torch.FloatTensor(weights).to(DEVICE)

    # --- Model ---
    model = SkinDiseaseResNet(num_classes=num_classes, pretrained=True).to(DEVICE)

    # --- Optimization ---
    criterion = nn.CrossEntropyLoss(weight=class_weights)
    optimizer = optim.Adam(model.parameters(), lr=LR, weight_decay=1e-4)
    scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='min', factor=0.1, patience=2)

    # --- Trainer ---
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

    # 🔄 Auto-Resume from latest checkpoint
    start_epoch = trainer.load_latest_checkpoint()

    # --- Start Training ---
    print(f"🚀 Fine-tuning ResNet-50 on {DEVICE}...")
    trainer.fit(epochs=EPOCHS, start_epoch=start_epoch)

if __name__ == "__main__":
    main()
