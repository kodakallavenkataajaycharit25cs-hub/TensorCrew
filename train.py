import torch
import torch.nn as nn
import torch.optim as optim
from dataset.dataset_loader import get_loaders
from model.custom_nn import SkinDiseaseResNet
from training.trainer import Trainer
from collections import Counter
import os

def main():
    EPOCHS = 30
    BATCH_SIZE = 32
    LR = 0.0001 
    DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'

    if not os.path.exists('checkpoints'):
        os.makedirs('checkpoints')

    train_loader, val_loader, _, classes = get_loaders()
    num_classes = len(classes)

    targets = [y for _, y in train_loader.dataset.samples]
    count = Counter(targets)
    total_samples = sum(count.values())
    weights = [total_samples / (num_classes * count[i]) for i in range(num_classes)]
    class_weights = torch.FloatTensor(weights).to(DEVICE)

    model = SkinDiseaseResNet(num_classes=num_classes, pretrained=True)
    
    for param in model.model.parameters():
        param.requires_grad = False
    for param in model.model.layer4.parameters():
        param.requires_grad = True
    for param in model.model.fc.parameters():
        param.requires_grad = True
        
    model = model.to(DEVICE)

    criterion = nn.CrossEntropyLoss(weight=class_weights)
    optimizer = optim.Adam(filter(lambda p: p.requires_grad, model.parameters()), lr=LR, weight_decay=5e-4)
    scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='min', factor=0.1, patience=2)

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

    print(f"Training ResNet-50 on {DEVICE}...")
    trainer.fit(epochs=EPOCHS, start_epoch=start_epoch)

if __name__ == "__main__":
    main()
