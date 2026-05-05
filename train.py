import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import WeightedRandomSampler
from dataset.dataset_loader import get_loaders
from model.custom_nn import SkinDiseaseModel
from training.trainer import Trainer, FocalLoss
from collections import Counter
import os

def main():
    EPOCHS = 100
    BATCH_SIZE = 16
    LR = 3e-4
    DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'

    if not os.path.exists('checkpoints'):
        os.makedirs('checkpoints')

    train_loader, val_loader, _, classes = get_loaders(batch_size=BATCH_SIZE)
    num_classes = len(classes)

    # Calculate class weights for Sampler and Loss
    targets = [y for _, y in train_loader.dataset.samples]
    count = Counter(targets)
    class_count = [count[i] for i in range(num_classes)]
    
    # 1. Weighted Random Sampler (Handles Imbalance in Batching)
    weights = [1.0 / count[y] for y in targets]
    sampler = WeightedRandomSampler(weights, len(weights))
    
    # Re-create train loader with sampler
    train_loader = torch.utils.data.DataLoader(
        train_loader.dataset, batch_size=BATCH_SIZE, sampler=sampler
    )

    # 2. Loss Weights
    total_samples = sum(class_count)
    loss_weights = torch.FloatTensor([total_samples / c for c in class_count]).to(DEVICE)

    model = SkinDiseaseModel(num_classes=num_classes)
    model = model.to(DEVICE)

    # 3. Use Focal Loss
    criterion = FocalLoss(weight=loss_weights, gamma=2.0)
    
    optimizer = optim.AdamW(model.parameters(), lr=LR, weight_decay=1e-2)
    scheduler = optim.lr_scheduler.CosineAnnealingWarmRestarts(optimizer, T_0=10, T_mult=2)

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

    start_epoch = trainer.load_latest_checkpoint()

    print(f"Training DSC Model on {DEVICE} for {num_classes} classes...")
    trainer.fit(epochs=EPOCHS, start_epoch=start_epoch)

if __name__ == "__main__":
    main()
