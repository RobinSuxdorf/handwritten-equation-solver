import torch
import torch.nn as nn
import torch.nn.functional as F

class SymbolClassifier(nn.Module):
    def __init__(self) -> None:
        super().__init__()
        self.conv1 = nn.Conv2d(1, 10, kernel_size=5)
        self.conv2 = nn.Conv2d(10, 20, kernel_size=5)
        self.pool = nn.MaxPool2d(2, 2)
        self.fc1 = nn.Linear(320, 50)
        self.fc2 = nn.Linear(50, 10)

    def forward(
        self,
        x: torch.tensor # (batch_size, 1, 28, 28)
    ) -> torch.tensor: # (batch_size, 10)
        x = self.pool(F.relu(self.conv1(x))) # (batch_size, 10, 12, 12)
        x = self.pool(F.relu(self.conv2(x))) # (batch_size, 20, 4, 4)
        x = torch.flatten(x, 1) # (batch_size, 320)
        x = self.fc1(x) # (batch_size, 50)
        x = self.fc2(x) # (batch_size, 10)
        return F.softmax(x, dim=1)
