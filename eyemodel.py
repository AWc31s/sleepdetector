import torch
import torch.nn as nn
import torch.nn.functional as F

class EyeModel(nn.Module):
    def __init__(self):
        super().__init__()
#         self.conv1 = nn.Conv2d(1, 5, 3)
        self.conv1 = nn.Conv2d(1, 24, 3)
        self.pool = nn.MaxPool2d(2, 2)
#         self.conv2 = nn.Conv2d(5, 7, 3)
        self.conv2 = nn.Conv2d(24, 48, 3)
#         self.fc1 = nn.Linear(112, 2)
        self.fc1 = nn.Linear(768, 2)

    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = torch.flatten(x, 1) # flatten all dimensions except batch
        x = self.fc1(x)
        return x
