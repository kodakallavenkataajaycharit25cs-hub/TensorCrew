import torch
import torch.nn as nn
from torchvision import models
from torchvision.models import EfficientNet_V2_S_Weights

class AdaptiveConcatPool2d(nn.Module):
    """
    Concatenates AdaptiveAvgPool2d and AdaptiveMaxPool2d.
    Helps capture both global texture (avg) and strong local features (max).
    """
    def __init__(self, output_size=1):
        super().__init__()
        self.avg = nn.AdaptiveAvgPool2d(output_size)
        self.max = nn.AdaptiveMaxPool2d(output_size)

    def forward(self, x):
        return torch.cat([self.avg(x), self.max(x)], 1)

class SkinDiseaseModel(nn.Module):
    def __init__(self, num_classes=7, pretrained=True):
        super(SkinDiseaseModel, self).__init__()
        
        if pretrained:
            base_model = models.efficientnet_v2_s(weights=EfficientNet_V2_S_Weights.DEFAULT)
        else:
            base_model = models.efficientnet_v2_s(weights=None)

        # Extract features (exclude the original avgpool and classifier)
        self.features = base_model.features
        
        # Original features output 1280 channels for EfficientNet-V2-S
        num_ftrs = 1280 

        # Upgrade 1: Adaptive Concat Pooling
        # Concatenating Avg and Max pooling doubles the features (1280 * 2 = 2560)
        self.pool = AdaptiveConcatPool2d(output_size=1)
        self.flatten = nn.Flatten()

        # Upgrade 2: Deeper Classifier Head
        # Higher capacity mapping: 2560 -> 512 -> num_classes
        self.classifier = nn.Sequential(
            nn.BatchNorm1d(num_ftrs * 2),
            nn.Dropout(p=0.3),
            nn.Linear(num_ftrs * 2, 512),
            nn.ReLU(inplace=True),
            nn.BatchNorm1d(512),
            nn.Dropout(p=0.4),
            nn.Linear(512, num_classes)
        )

    def forward(self, x):
        x = self.features(x)
        x = self.pool(x)
        x = self.flatten(x)
        x = self.classifier(x)
        return x

if __name__ == "__main__":
    model = SkinDiseaseModel(num_classes=7)
    model.eval() # Added to avoid BatchNorm errors with batch size 1
    dummy_img = torch.randn(1, 3, 224, 224)
    output = model(dummy_img)
    print(f"Output Shape: {output.shape}")
    
    total_params = sum(p.numel() for p in model.parameters())
    trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
    print(f"Total Params: {total_params:,}")
    print(f"Trainable Params: {trainable_params:,}")
