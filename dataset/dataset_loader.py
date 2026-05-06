import torch
from torchvision import datasets, transforms
from torch.utils.data import DataLoader
from pathlib import Path

TRAIN_DIR = Path("Data/train")
VAL_DIR = Path("Data/val")
TEST_DIR = Path("Data/test")

IMAGE_SIZE = 224
BATCH_SIZE = 16

# HAM10000 normalization constants
MEAN = [0.763, 0.546, 0.570]
STD = [0.141, 0.153, 0.169]

train_transforms = transforms.Compose([
    transforms.RandomResizedCrop(IMAGE_SIZE),
    transforms.RandomHorizontalFlip(),
    transforms.RandomVerticalFlip(),
    transforms.RandomRotation(20),
    transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2, hue=0.1),
    transforms.ToTensor(),
    transforms.Normalize(MEAN, STD)
])

val_test_transforms = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(IMAGE_SIZE),
    transforms.ToTensor(),
    transforms.Normalize(MEAN, STD)
])

def get_loaders(batch_size=BATCH_SIZE):
    train_dataset = datasets.ImageFolder(TRAIN_DIR, transform=train_transforms)
    val_dataset = datasets.ImageFolder(VAL_DIR, transform=val_test_transforms)
    test_dataset = datasets.ImageFolder(TEST_DIR, transform=val_test_transforms)
    
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False)
    test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)
    return train_loader, val_loader, test_loader, train_dataset.classes

if __name__ == "__main__":
    train_loader, val_loader, test_loader, classes = get_loaders()
    print(f"Found {len(classes)} classes.")
    print(f"Loaded {len(train_loader.dataset)} training images.")
