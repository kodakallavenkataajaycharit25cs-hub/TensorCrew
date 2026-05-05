import torch
import torch.nn as nn

class DepthwiseSeparableConv(nn.Module):
    def __init__(self, in_channels, out_channels, stride=1):
        super().__init__()
        self.depthwise = nn.Conv2d(
            in_channels, in_channels, kernel_size=3, 
            stride=stride, padding=1, groups=in_channels, bias=False
        )
        self.pointwise = nn.Conv2d(
            in_channels, out_channels, kernel_size=1, 
            stride=1, padding=0, bias=False
        )
        self.bn = nn.BatchNorm2d(out_channels)
        self.relu = nn.ReLU(inplace=True)

    def forward(self, x):
        x = self.depthwise(x)
        x = self.pointwise(x)
        x = self.bn(x)
        x = self.relu(x)
        return x

class AdaptiveConcatPool2d(nn.Module):
    def __init__(self, output_size=1):
        super().__init__()
        self.avg = nn.AdaptiveAvgPool2d(output_size)
        self.max = nn.AdaptiveMaxPool2d(output_size)

    def forward(self, x):
        return torch.cat([self.avg(x), self.max(x)], 1)

class SkinDiseaseModel(nn.Module):
    def __init__(self, num_classes=23):
        super(SkinDiseaseModel, self).__init__()
        
        self.features = nn.Sequential(
            # Initial stem
            nn.Conv2d(3, 32, kernel_size=3, stride=2, padding=1, bias=False),
            nn.BatchNorm2d(32),
            nn.ReLU(inplace=True),
            
            # DSC Blocks
            DepthwiseSeparableConv(32, 64, stride=1),
            DepthwiseSeparableConv(64, 128, stride=2),
            DepthwiseSeparableConv(128, 128, stride=1),
            DepthwiseSeparableConv(128, 256, stride=2),
            DepthwiseSeparableConv(256, 256, stride=1),
            DepthwiseSeparableConv(256, 512, stride=2),
            DepthwiseSeparableConv(512, 512, stride=1),
            DepthwiseSeparableConv(512, 1024, stride=2),
            DepthwiseSeparableConv(1024, 1024, stride=1),
        )

        self.pool = AdaptiveConcatPool2d(output_size=1)
        self.flatten = nn.Flatten()

        self.classifier = nn.Sequential(
            nn.BatchNorm1d(1024 * 2),
            nn.Dropout(p=0.3),
            nn.Linear(1024 * 2, 512),
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
    model = SkinDiseaseModel(num_classes=23)
    model.eval()
    dummy_img = torch.randn(1, 3, 224, 224)
    output = model(dummy_img)
    print(f"Output Shape: {output.shape}")
    
    total_params = sum(p.numel() for p in model.parameters())
    print(f"Total Params: {total_params:,}")
