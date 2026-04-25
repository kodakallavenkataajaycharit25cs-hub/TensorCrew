import torch
import torch.nn as nn
from torchvision import models
from torchvision.models import EfficientNet_V2_S_Weights

class SkinDiseaseModel(nn.Module):
    def __init__(self, num_classes=7, pretrained=True):
        super(SkinDiseaseModel, self).__init__()
        
        if pretrained:
            self.model = models.efficientnet_v2_s(weights=EfficientNet_V2_S_Weights.DEFAULT)
        else:
            self.model = models.efficientnet_v2_s(weights=None)

        num_ftrs = self.model.classifier[1].in_features

        self.model.classifier = nn.Sequential(
            nn.Dropout(p=0.4, inplace=True),
            nn.Linear(num_ftrs, num_classes)
        )

    def forward(self, x):
        return self.model(x)

if __name__ == "__main__":
    model = SkinDiseaseModel(num_classes=7)
    dummy_img = torch.randn(1, 3, 224, 224)
    output = model(dummy_img)
    print(f"Output Shape: {output.shape}")
    
    total_params = sum(p.numel() for p in model.parameters())
    trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
    print(f"Total Params: {total_params:,}")
    print(f"Trainable Params: {trainable_params:,}")
