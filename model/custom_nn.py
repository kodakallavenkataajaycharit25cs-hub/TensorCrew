import torch
import torch.nn as nn
from torchvision import models

class SkinDiseaseModel(nn.Module):
    def __init__(self, num_classes=7, pretrained=True):
        super(SkinDiseaseModel, self).__init__()
        # Using EfficientNet-B0 as the backbone - widely considered state-of-the-art for this scale
        if pretrained:
            self.backbone = models.efficientnet_b0(weights=models.EfficientNet_B0_Weights.IMAGENET1K_V1)
        else:
            self.backbone = models.efficientnet_b0(weights=None)
            
        # Replace the classifier head
        in_features = self.backbone.classifier[1].in_features
        self.backbone.classifier = nn.Sequential(
            nn.Dropout(p=0.4, inplace=True),
            nn.Linear(in_features, num_classes)
        )

    def forward(self, x):
        return self.backbone(x)

if __name__ == "__main__":
    # Test for HAM10000 (7 classes)
    model = SkinDiseaseModel(num_classes=7, pretrained=False)
    model.eval()
    dummy_img = torch.randn(1, 3, 224, 224)
    output = model(dummy_img)
    print(f"Output Shape: {output.shape}")
    
    total_params = sum(p.numel() for p in model.parameters())
    print(f"Total Params: {total_params:,}")
