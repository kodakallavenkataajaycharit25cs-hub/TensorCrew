import torch
import torch.nn as nn
from torchvision import models
from torchvision.models import ResNet50_Weights

class SkinDiseaseResNet(nn.Module):
    def __init__(self, num_classes=23, pretrained=True):
        super(SkinDiseaseResNet, self).__init__()
        
        if pretrained:
            self.model = models.resnet50(weights=ResNet50_Weights.DEFAULT)
        else:
            self.model = models.resnet50(weights=None)

        num_ftrs = self.model.fc.in_features

        self.model.fc = nn.Sequential(
            nn.Dropout(0.5), 
            nn.Linear(num_ftrs, num_classes)
        )

    def forward(self, x):
        return self.model(x)

if __name__ == "__main__":
    model = SkinDiseaseResNet(num_classes=23)
    dummy_img = torch.randn(1, 3, 224, 224)
    output = model(dummy_img)
    print(f"Output Shape: {output.shape}")
    
    total_params = sum(p.numel() for p in model.parameters())
    trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
    print(f"Total Params: {total_params:,}")
    print(f"Trainable Params: {trainable_params:,}")
