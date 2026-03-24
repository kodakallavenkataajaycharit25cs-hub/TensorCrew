import torch
from torchvision import datasets, transforms
from torch.utils.data import DataLoader
from pathlib import Path

TRAIN_DIR = Path("Data/train")
VAL_DIR = Path("Data/val")
TEST_DIR = Path("Data/test")

IMAGE_SIZE = 224
BATCH_SIZE = 32

train_transforms = transforms.Compose([
  transforms.Resize((IMAGE_SIZE, IMAGE_SIZE)),
  transforms.RandomHorizontalFlip(p= 0.5), # 50% chance
  transforms.RandomRotation(degrees= 15), # +15/-15 
  transforms.ToTensor(),
  transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

val_test_transforms = transforms.Compose([
  transforms.Resize((IMAGE_SIZE, IMAGE_SIZE)),
  transforms.ToTensor(),
  transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

def get_loaders():
  train_dataset = datasets.ImageFolder(TRAIN_DIR, transform= train_transforms)
  val_dataset = datasets.ImageFolder(VAL_DIR, transform= val_test_transforms)
  test_dataset = datasets.ImageFolder(TEST_DIR, transform= val_test_transforms)
  
  train_loader = DataLoader(train_dataset, batch_size= BATCH_SIZE, shuffle= True)
  val_loader = DataLoader(val_dataset,batch_size= BATCH_SIZE, shuffle= False )
  test_loader = DataLoader(test_dataset, batch_size= BATCH_SIZE, shuffle= False)
  return train_loader, val_loader, test_loader, train_dataset.classes

if __name__ == "__main__":
  train_loader, val_loader, test_loader, classes = get_loaders()
  print(f"Found {len(classes)} classes: {classes[:3]}...")
  print(f"Loaded {len(train_loader.dataset)} training images.")