import torch
import torch.nn as nn
from efficientnet_pytorch_3d import EfficientNet3D
from torchvision.models import resnet50, ResNet50_Weights
from torchvision.models import vgg16, VGG16_Weights

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')


class OCTCNN(nn.Module):
    def __init__(self, num_classes, num_channels=1,
                 out_channels=[32, 64, 128],
                 kernel_sizes=[3, 3, 3],
                 stride_sizes=[2, 2, 2],
                 dropout=0.1):
        super(OCTCNN, self).__init__()

        layers = []
        prev_channels = num_channels
        for i in range(len(out_channels)):
            layers.append(nn.Conv2d(prev_channels, out_channels[i], kernel_size=kernel_sizes[i], stride=stride_sizes[i], padding=kernel_sizes[i] // 2))
            layers.append(nn.ReLU())
            layers.append(nn.BatchNorm2d(out_channels[i]))  # Batch Normalization
            layers.append(nn.MaxPool2d(kernel_size=2, stride=2))
            prev_channels = out_channels[i]

        self.model = nn.Sequential(*layers)
        self.avg_pool = nn.AdaptiveAvgPool2d(3)
        self.fc_layers = nn.Sequential(
            nn.Linear(out_channels[-1] * 3 * 3, 128),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(128, num_classes)
        )

    def forward(self, x):
        x = self.model(x)
        x = self.avg_pool(x)
        x = torch.flatten(x, 1)
        x = self.fc_layers(x)
        return x


def getModel(model_name, num_classes, num_channels=1, out_channels=[32, 64, 128], kernel_sizes=[3, 3, 3], stride_sizes=[2, 2, 2], dropout=0.1):
    match model_name:
        case 'CNN2D':
            return OCTCNN(num_classes, num_channels, out_channels, kernel_sizes, stride_sizes, dropout)
        case 'CNN3D':
            return EfficientNet3D.from_name("efficientnet-b1", override_params={'num_classes': num_classes}, in_channels=3)
        case 'ResNet50':
            model = resnet50(weights=ResNet50_Weights.DEFAULT)
            model = model.to(device)
            model.fc = nn.Linear(model.fc.in_features, num_classes)
            return model
        case 'VGG16':
            model = vgg16(weights=VGG16_Weights.DEFAULT)
            model = model.to(device)
            model.classifier[6] = nn.Linear(model.classifier[6].in_features, num_classes)
            return model


