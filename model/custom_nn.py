import torch
import torch.nn as nn

class SkinDiseaseCNN(nn.Module):
    def __init__(self, num_classes=23):
        super(SkinDiseaseCNN, self).__init__()
        
        # --- 4-Layer Feature Extractor ---
        self.features = nn.Sequential(
            # Block 1: 224 -> 112
            nn.Conv2d(3, 32, kernel_size=3, padding=1),
            nn.BatchNorm2d(32),
            nn.ReLU(),
            nn.MaxPool2d(2, 2),

            # Block 2: 112 -> 56
            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(),
            nn.MaxPool2d(2, 2),

            # Block 3: 56 -> 28
            nn.Conv2d(64, 128, kernel_size=3, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(),
            nn.MaxPool2d(2, 2),

            # Block 4: 28 -> 14
            nn.Conv2d(128, 256, kernel_size=3, padding=1),
            nn.BatchNorm2d(256),
            nn.ReLU(),
            nn.MaxPool2d(2, 2), # Final size: 14x14
            
            # --- Global Average Pooling (GAP) ---
            # Instead of flattening 256*14*14, we average each filter map to a single value.
            nn.AdaptiveAvgPool2d(1) # Result: [Batch, 256, 1, 1]
        )
        
        # --- Compact Classifier ---
        self.classifier = nn.Sequential(
            nn.Flatten(),
            nn.Linear(256, 128), # Much lighter than before!
            nn.ReLU(),
            nn.Dropout(0.4),
            nn.Linear(128, num_classes)
        )

    def forward(self, x):
        return self.classifier(self.features(x))

if __name__ == "__main__":
    model = SkinDiseaseCNN(num_classes=23)
    dummy_img = torch.randn(1, 3, 224, 224)
    output = model(dummy_img)
    print(f"✅ Output Shape: {output.shape}")
    total_params = sum(p.numel() for p in model.parameters())
    print(f"✅ Total Params: {total_params:,} (MUCH lighter!)")
