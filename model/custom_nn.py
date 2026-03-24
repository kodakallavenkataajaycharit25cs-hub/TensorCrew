import torch
import torch.nn as nn
from tqdm import tqdm
import time

class AdaptiveConcatPool2d(nn.Module):
    def __init__(self, sz=1):
        super().__init__()
        self.ap = nn.AdaptiveAvgPool2d(sz)
        self.mp = nn.AdaptiveMaxPool2d(sz)

    def forward(self, x):
        return torch.cat([self.mp(x), self.ap(x)], 1)

class SkinDiseaseCNN(nn.Module):
    def __init__(self, num_classes=23):
        super(SkinDiseaseCNN, self).__init__()

        self.features = nn.Sequential(
            nn.Conv2d(3, 32, kernel_size=3, padding=1),
            nn.BatchNorm2d(32),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2),
            
            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2),

            nn.Conv2d(64, 128, kernel_size=3, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2),

            nn.Conv2d(128, 256, kernel_size=3, padding=1),
            nn.BatchNorm2d(256),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2),

            nn.Conv2d(256, 512, kernel_size=3, padding=1),
            nn.BatchNorm2d(512),
            nn.ReLU(),
            
            AdaptiveConcatPool2d(1)
        )

        self.classifier = nn.Sequential(
            nn.Flatten(),
            nn.Linear(1024, 512),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(512, 256),
            nn.ReLU(),
            nn.Dropout(0.3), 
            nn.Linear(256, num_classes)
        )

    def forward(self, x):
        x = self.features(x)
        x = self.classifier(x)
        return x
  
if __name__ == "__main__":
    print("="*40)
    print("🚀 INITIALIZING MODEL SANITY CHECK...")
    model = SkinDiseaseCNN(num_classes=23)
    
    num_test_batches = 10
    batch_size = 32
    
    print(f"🧪 Testing model with {num_test_batches} batches of {batch_size} images...")
    
    for i in tqdm(range(num_test_batches), desc="Processing Batches"):
        dummy_batch = torch.randn(batch_size, 3, 224, 224)
        output = model(dummy_batch)
        time.sleep(0.05)

    print("\n✅ MODEL INITIALIZED WITH DUAL POOLING!")
    print(f"✅ Final Output Shape: {output.shape} (Must be [32, 23])")
    
    total_params = sum(p.numel() for p in model.parameters())
    print(f"✅ Total Params: {total_params:,}")
    print("="*40)
