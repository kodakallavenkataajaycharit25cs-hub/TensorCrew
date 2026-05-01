import torch
import torch.nn as nn
import torch.optim as optim
from dataset.dataset_loader import get_loaders
from model.custom_nn import SkinDiseaseModel
from training.trainer import Trainer
from collections import Counter
import os

def main():
    EPOCHS = 50
    BATCH_SIZE = 16
    LR = 1e-4
    DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'

    if not os.path.exists('checkpoints'):
        os.makedirs('checkpoints')

    train_loader, val_loader, _, classes = get_loaders(batch_size=BATCH_SIZE)
    num_classes = len(classes)

    targets = [y for _, y in train_loader.dataset.samples]
    count = Counter(targets)
    total_samples = sum(count.values())
    weights = [total_samples / (num_classes * count[i]) for i in range(num_classes)]
    class_weights = torch.FloatTensor(weights).to(DEVICE)

    model = SkinDiseaseModel(num_classes=num_classes, pretrained=True)
    
    # Ensure all parameters are trainable
    for param in model.parameters():
        param.requires_grad = True
        
    model = model.to(DEVICE)

    criterion = nn.CrossEntropyLoss(weight=class_weights, label_smoothing=0.1)
    optimizer = optim.AdamW(model.parameters(), lr=LR, weight_decay=1e-3)
    scheduler = optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=EPOCHS)

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

    print(f"Training EfficientNet-V2 on {DEVICE}...")
    trainer.fit(epochs=EPOCHS, start_epoch=start_epoch)

if __name__ == "__main__":
    main()
